import cryptocode

test = cryptocode.encrypt("pass3", "7804FCE44075FD6F8A014E31665B1E1E56BC16BE")
user = cryptocode.decrypt("s8P5HIE=*uhoaQvYErekMjEhWvMOEWg==*VBYVwc/0UpOSWtE6iVU6bw==*agU+7nIOkh3g2rg8BU280A==", "7804FCE44075FD6F8A014E31665B1E1E56BC16BE")

print(test)
print(user)