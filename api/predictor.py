import torch
import torch.nn as nn


import os
from PIL import Image
import cv2
from torchvision import transforms

class GRU(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes, device):
        super(GRU, self).__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.device = device
        # -> x needs to be: (batch_size, seq, input_size)
        
        # or:
        #self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        #self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

        self.double()
        
    def forward(self, x):
        # Set initial hidden states (and cell states for LSTM)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(self.device).double()
        
        
        # x: (n, 28, 28), h0: (2, n, 128)
        
        # Forward propagate RNN
        out, _ = self.gru(x, h0)
        # or:
        #out, _ = self.lstm(x, (h0,c0))  
        
        # out: tensor of shape (batch_size, seq_length, hidden_size)
        # out: (n, 28, 128)
        
        # Decode the hidden state of the last time step
        out = out[:, -1, :]
        # out: (n, 128)
         
        out = self.fc(out)
        # out: (n, 10)
        return out



def get_prediction(images):
    # define device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    #define model paramerters
    input_size = 28
    sequence_length = 28
    hidden_size = 128
    num_layers = 2
    num_classes = 10

    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model/') + 'best_0.pth'

    if os.path.exists(model_path):
        print(" Weights are found ")
    else:
        print("\n\n\n\n Did not find weights \n\n filepath ", model_path, "\n\n\n")
        return None

    #define model
    model = GRU(input_size, hidden_size, num_layers, num_classes, device)

    model = model.to(device)

    model.load_state_dict(torch.load(model_path, map_location="cpu"))

    model.eval()

    digits=[]

    transform = transforms.Compose([
                        transforms.PILToTensor()
                    ])

    for img in images:

        img = Image.fromarray(img)

        img = transform(img).squeeze()

        img = img.double()

        img = torch.div(img, 255)

        img = img.to(device)

        img = img.view(1, 28, 28)

        output = model(img)

        _, predicted = torch.max(output.data, 1)

        digits.append(predicted.cpu().numpy()[0])

    final_number = ''.join(map(str, digits))

    return final_number


