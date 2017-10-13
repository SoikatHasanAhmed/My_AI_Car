# My_AI_Car
Self driving Rc car with raspberry pi and tf learn and opencv with cnn


i am trying to drive the car with the cnn by only camera feed .

Raspberry Pi Codes
video server.py // it just send the image over TCP and the clint (my pc) receive it

car_control_server :
  i use a game pad for manual control to run the car and take analog values -1 - 1 and convert them 100 - 300 and
  receive the value from pc and write some condition to drive the car it send back data = 200 it means it is working good
  
PC codes :

car_control.py (pc clint) // receive the gamepad value and just send over tcp to  car_control_server


data_collect_client.py // it receive the video from the video server also the gamepad value (F/left/right) and save
them in .npy file

manage_train_data.py // it manage the train data and random the data amd make a final .npy file


train.py //to train the model 
test_car_model.py // to test the car with the model ....

  
