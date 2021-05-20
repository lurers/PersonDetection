import sensor,image,lcd,time
import KPU as kpu

lcd.init(type=2)
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
#sensor.set_vflip(1) #flip camera; maix go use sensor.set_hmirror(0)
sensor.set_hmirror(1)
sensor.set_vflip(1)
sensor.run(1)
clock = time.clock()
classes = ['person']
task = kpu.load(0x800000)
anchor = (1.08, 1.19, 3.42, 4.41, 6.63, 11.38, 9.42, 5.11, 16.62, 10.52)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
while(True):
    clock.tick()
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    print(clock.fps())
    if code:
        for i in code:
            a=img.draw_rectangle(i.rect())
            a = lcd.display(img)
            a=img.draw_string(i.x(), i.y()+12, 'Person', color=(0, 0, 0), scale=3)
            for i in code:
                lcd.draw_string(i.x(), i.y()+12, 'Person', lcd.RED, lcd.WHITE)

    else:
        a = lcd.display(img)
a = kpu.deinit(task)
