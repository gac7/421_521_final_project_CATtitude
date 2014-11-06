CATTITUDE: A selective cat spraying device for behavior training
========

Brainstorm
----
            We propose developing a device which will detect the presence of a cat and subsequently trigger the spraying of water in the general direction of the cat. We will use a Raspbeery Pi camera with firmware that we will develop to recognize when a cat appears in the camera’s viewfield. Detection of a cat will initiate a program that communicates with Arduino to activate an actuator which squeezes the handle of a squirt gun, thereby deploying water onto the cat.

In addition to basic spraying functionality, we will provide key features for users. Retention of the cat detection images will result in cat criminal mugshots. We will upload these onto the blog CATastropheAvoided.tumblr.com for the benefit of society (broader impacts). We will also provide an alert system to send emails to the owner when the sprayer needs to be refilled. Finally, a comprehensive log file of spraying events will be accessible and emailed to the owner weekly. 

![CATtitude Flow Chart](https://github.com/gac7/421_521_final_project_CATtitude/Images/CATtitude_flow.jpg)

Abstract
----

 We aim to improve the behavior of growing domestic cats by developing a device that will detect their presence which will trigger a water squirt response in the general direction of the cat. The device will be strategically placed in a no-cat zone such as a kitchen countertop where some cats tend to pry unwarrantedly such that the cat will be trained to no longer breach said boundaries. We will use a Raspberry Pi camera with firmware that we will develop based off Open Source Computer Vision (OpenCV) to recognize the cat’s presence once within the camera’s field of view. Once detected, the device will trigger a water squirt response by initiating a program that communicates with Arduino to activate a 12V Plastic Water Solenoid Valve to open and thereby deploying water onto the cat.
            Additionally, we propose to include key features to improve user-device interface. In order to keep track of the user’s misbehaving cat, the camera will snap criminal mugshots to keep a running Guilt CATalog as well as weekly email alerts with a comprehensive log file of all water deployment instances. These photos will be uploaded to the blog: CATastopheAvoided.tumblr.com for the benefit of society. We will also include an alert system to send emails to the user when the water reservoir needs refilling. By utilizing this device, users will have the peace of mind of knowing that the device is continuously armed and ready to train their misbehaving cats.