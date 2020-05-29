import paypalrestsdk
from paypalrestsdk import Payout, ResourceNotFound
import random 
import string


sender_batch_id =''.join(
    random.choice(string.ascii_uppercase) for i in range(12)
        
    )

# paypalrestsdk.configure({
    
#   "mode": "sandbox", # sandbox or live
#   "client_id": "AQleHmqLc9f9njvGRJPACaEfqMew9SErmJmpT1G4nsjKa5zpNvVeZFlABB-zmn95oztxl9KqbR4Ekvm0",
#   "client_secret": "EPLTC2LWgRoMPcOaQqH-iSvxxg6QZMva5aeIYuTa7Z-2pHMyz93os4yCefCf5WyrfIJ7tJrnyu-PETbD" })
paypalrestsdk.configure({
    
  "mode": "live", # sandbox or live
  "client_id": "AdLKr0lXh2gM0lLrATlSUX_y-hmBdC8BVyGXa8foNItyrfQgiXcu9GX6iJXsovOqMumvpL8Jzth02E5o",
  "client_secret": "EJytRi9KmxPUad2ZsumW7l0Ttgg0T_UVuxOw-fCPXyV6gPc_nyi6U7TUuEJa1Dibwdl93e2q7PonTdlk" })

def paypal_payout_release(items):
    items = items

    payout = Payout({
        "sender_batch_header": {
            "sender_batch_id": sender_batch_id,
            "email_subject": "You have a payment"
        },
        "items":items
    })

    if payout.create(sync_mode=False):
        print("payout[%s] created successfully" %
            (payout.batch_header.payout_batch_id))
    else:
        print(payout.error)


