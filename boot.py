import sensor,image,lcd,time
import KPU as kpu
from machine import I2C

count = 0

def on_receive(data):
    print("on_receive:",data)

def on_transmit():
    count = count+1
    print("on_transmit, send:",count)
    return count

def on_event(event):
    print("on_event:",event)

i2c = I2C(I2C.I2C0, mode=I2C.MODE_SLAVE, scl=30, sda=31, addr=0x24, addr_size=7, on_receive=on_receive, on_transmit=on_transmit, on_event=on_event)

lcd.init(type=2)
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)
sensor.set_vflip(1)
sensor.run(1)
clock = time.clock()
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
task = kpu.load(0x800000)
anchor = (1.08, 1.19, 3.42, 4.41, 6.63, 11.38, 9.42, 5.11, 16.62, 10.52)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
dataperson = 0
while(True):
    clock.tick()
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    #print(clock.fps())
    if code:
        for i in code:
            if (i.classid()==14):
                dataperson=1
                print(dataperson)
            else:
                dataperson=0
                print(dataperson)
            a=img.draw_rectangle(i.rect())
            a = lcd.display(img)
            a=img.draw_string(i.x(), i.y()+12, classes[i.classid()], color=(0, 0, 0), scale=3)

            for i in code:
                lcd.draw_string(i.x(), i.y(), classes[i.classid()], lcd.RED, lcd.WHITE)



    else:
        a = lcd.display(img)
a = kpu.deinit(task)


