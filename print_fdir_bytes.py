with open(r"S:\cre\Devices.Tycoon\Devices.Tycoon\Devices Tycoon\www\assets.dat", "rb") as f:
    f.seek(16 + 4 + 8 + 4)
    data = f.read(250)
    print("Raw bytes:")
    print(data)
