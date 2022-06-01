import torch, torchvision
import torch.nn as nn
from torchvision import transforms
import albumentations
import albumentations.pytorch
import cv2
from torchvision.transforms import ToTensor

# --------------------- ResNet moel ---------------------
# 3x3 convolution
def conv3x3(in_channels, out_channels, stride=1):
    return nn.Conv2d(in_channels, out_channels, kernel_size=3, 
                     stride=stride, padding=1, bias=False)

# Residual block
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super(ResidualBlock, self).__init__()
        self.conv1 = conv3x3(in_channels, out_channels, stride)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(out_channels, out_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.downsample = downsample

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        if self.downsample:
            residual = self.downsample(x)
        out += residual
        out = self.relu(out)
        return out

# ResNet
class ResNet(nn.Module):
    def __init__(self, block, layers, num_classes=7):
        super(ResNet, self).__init__()
        self.in_channels = 16
        self.conv = conv3x3(3, 16)
        self.bn = nn.BatchNorm2d(16)
        self.relu = nn.ReLU(inplace=True)
        self.layer1 = self.make_layer(block, 16, layers[0])
        self.layer2 = self.make_layer(block, 32, layers[1], 2)
        self.layer3 = self.make_layer(block, 64, layers[2], 2)
        self.avg_pool = nn.AvgPool2d(8)
        self.fc = nn.Linear(64, num_classes)

    def make_layer(self, block, out_channels, blocks, stride=1):
        downsample = None
        if (stride != 1) or (self.in_channels != out_channels):
            downsample = nn.Sequential(
                conv3x3(self.in_channels, out_channels, stride=stride),
                nn.BatchNorm2d(out_channels))
        layers = []
        layers.append(block(self.in_channels, out_channels, stride, downsample))
        self.in_channels = out_channels
        for i in range(1, blocks):
            layers.append(block(out_channels, out_channels))
        return nn.Sequential(*layers)

    def forward(self, x):
        out = self.conv(x)
        out = self.bn(out)
        out = self.relu(out)
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.avg_pool(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out

# --------------------- 이미지로부터 감정 추출 ---------------------
# input: 인스타로부터 얻은 게시물 이미지, output: 감정 label -> 0:anger, 1:anxiety, 2:delight, 3:hurt, 4:panic, 5:sad 
def emotion_from_image(img):

    # 이미지에서 표정만 추출
    # haarcascade 불러오기
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # 이미지 불러오기
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 얼굴 찾기
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # 이미지에 사람이 없는 경우 -> 이미지 고려하지 않고 텍스트만 고려
    if len(faces) == 0:
        predicted = -1
    # 이미지에 여러명일 때 첫번째 표정만 고려
    else:
        (x, y, w, h) = faces[0]
        crop_img = img[y:y+h, x:x+w]

        # 미리 학습한 모델로 감정 예측
        model_image =  ResNet(ResidualBlock, [2, 2, 2])
        model_image.load_state_dict(torch.load('resnet_epoch80.pt', map_location=torch.device('cpu')))
        model_image.eval()
        
        #dataset_path = '/content/drive/MyDrive/img_temp/test/delight/test_delight_000.jpg' 
        #img = cv2.imread(dataset_path)
        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        albumentations_trans = albumentations.Compose(
            [albumentations.Resize(32, 32), 
            albumentations.pytorch.transforms.ToTensor()]
            )
        augmented = albumentations_trans(image=crop_img)
        trans_img = augmented['image']
        trans_img = torch.unsqueeze(trans_img, 0)

        outputs = model_image(trans_img)
        _, predicted = torch.max(outputs.data, 1)
        predicted = predicted.item()
    return predicted