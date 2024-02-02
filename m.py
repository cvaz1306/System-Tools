import sys_comms_refresh
print("Service started")
try:
    sys_comms_refresh.reset_interface(.1)
except KeyboardInterrupt:
    print("Service ended with keyboard.")
except:
    print("Error")