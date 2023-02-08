# WriteUp

#### This binary interested me because it gave me an opportunity to practice ret2libc challenges. I will try to be very thorough so that those who haven't understood ret2libc exploits can start to grasp it. 

#### Taking a look at the files provided, we see that we have a x64 binary (baby_boi) and also an "so" filed named libc-2.27.so. This gives a hint that the binary is dynamically linked. What this means is that if the binary does not have code that we can easily exploit, we can always resort to use the dynamically linked libraries. 

![Screenshot from 2021-09-28 09-49-53](https://user-images.githubusercontent.com/29875928/135113408-1f4cbf43-65d4-494d-8919-be6c56914f9e.png)

#### By using the checksec tool, we can find a little bit more about the exploit mitigations of this binary. 
* Partial RELRO
  * This means that we can overwrite the global offset table. For example, we can overwrite the GOT entry for puts, and have it jump to a function we want. We won't be using this, however
* No canary found
  * This means that we can create a buffer overflow without having to specify a special value called a canary. If this canary is overwritten, the program knows that we have abused the overflowed the stack.
* NX enabled
  * The NX bit is set meaning that the stack is non executable. This means that if we have a buffer overflow, we can't jump into the stack to execute code we would like.
* PIE
  * Position independent executable. The executable will be loaded at an unknown address. In this case because we don'thave PIE we know it will be looaded at 0x400000

#### Now let's run the program and see what we can exploit!

![Screenshot from 2021-09-28 10-13-45](https://user-images.githubusercontent.com/29875928/135116789-1bf9b960-ce05-4028-9db4-a726982dcfae.png)

#### After running it a couple times, we can see that we are greeted and then shown some kind of random address. Interestingly, the address seems to change every time we run it. Notice, however, that the offset at the end seems to be the same: 0xe10. This gives a hint that this is ASLR (Address Spacing Layout Randomization). This is an extra exploit mitigation technique that moves addresses of code around to make it harder for us to craft an exploit using hardcoded addresses. 

#### Let's take a look in IDA and see what we can find.
![Screenshot from 2021-09-28 10-28-45](https://user-images.githubusercontent.com/29875928/135118274-7febe5b2-770a-4004-a390-d1abbd7eefe3.png)

#### Here we can see that the weird hex characters that are given to us is actually the address of where the printf function is! Why is this important? printf is a part of the library libc. Libc is a cool library because we can use this library to exploit things we wouldn't be able to without it. For example, we can find the string "/bin/sh" in libc, as well as the function "system" which allows us to spawn a shell.

#### Now that we have the address of a function in libc, we can use this to locate the address of any other function we want, for example "system". Keep that in mind, but for now we need to craft a starting exploit. 

#### In the previous screenshot, after leaking the address of printf, the program asks you for input. In the form of the gets function. The gets function is something that you should always look out for because it allows for a user to input as many characters as they would like. The user can input characters past the size of the buffer size, overwriting local function variables, stack base pointer, and finally the stack return address. A safer function is the fgets function which forces the developer to specify how many bytes can be supplied by the user. Although this can also sometimes be vulnerable in that the developer may incorrectly allow for more bytes to be supplied than the size of the buffer.

#### Let's see how many bytes it takes to cause the program to crash. Instead of brute forcing input until we see the program crash, we can make use of the cyclic function in pwntools. This is a unique string which can guarantee that you can find the offset quickly because each part of the string is unique.

#### Generate cyclic string of size 1000
![Screenshot from 2021-09-28 10-41-08](https://user-images.githubusercontent.com/29875928/135120859-195f2897-cdc0-401f-b2e9-ab3e69e7339c.png)

#### Enter that string in input in gdb 
![Screenshot from 2021-09-28 10-42-41](https://user-images.githubusercontent.com/29875928/135120896-db1829cc-3067-45e2-a667-77f66b238c32.png)

#### Once the program has crashed, analyze the stack with x/4wx $rsp. Copy the 4 bytes located at the top of the stack and use that with cyclic_find to get the offset
![Screenshot from 2021-09-28 10-43-45](https://user-images.githubusercontent.com/29875928/135120918-ab35d569-d110-41b9-8ca8-d15a1d854edd.png)

#### We know that the program crashes after 40 bytes of input from the user. At the 41st byte, the program jumps to the address on the stack provided by the user. If bytes 41-44 are "AAAA", the program will try to jump to address 0x41414141 (the hex representation of 'A')

#### Now that we have control over the program, where do we want to jump to? We know that we want to call system with an argument of ("/bin/sh"). How do we provide arguments to functions? In x32 binaries it's quite easy, we can simply provide the argument in the stack. But since this is an x64 binary, arguments are provided through the registers. This means that we have to make use of a ROPgadget. What we want to do, is find a ROPgadget which will pop a value from the stack in to the register RDI. We can use the tool ROPgadget for this.

![Screenshot from 2021-09-28 10-57-07](https://user-images.githubusercontent.com/29875928/135123095-249d073b-4761-4ff4-b891-b742408b0fd7.png)

#### Here we piped the output into grep to filter only the results which have "pop rdi". Now we have everything we need to craft an exploit.

![Screenshot from 2021-09-28 11-01-00](https://user-images.githubusercontent.com/29875928/135123638-15a8c34b-61ab-48f5-bbe0-006544e17398.png)

#### Final Overview of the exploit script:
* Declare p to be the binary "baby_boi"
* have libc point to the libc binary being used. I didn't use the challenge libc since the CTF was not active
  * If you want to find the libc being used by your machine, use "ldd baby_boi" 
* In order to find the libcbase given the printf leak, we grab the offset where printf is located in in our local libc (once we have the libc base, we can find the system function by adding a known offset"
* Grab the leak from stdin and convert it into an integer representation
* Calculate the libc base with (printf_leak - printf_offset)
* Set the libc address to be equal to the libc base we just calculated
* Initialize the buffer overflow to having 40 bytes of padding ("A" * 40)
* overwrite the return address. Here I had to do stack alignment so I did an extra return instruction. (ropgadget_rdi + 1)
* Call the ropgadget to pop "/bin/sh" into rdi
* find where /bin/sh is located in the libc binary and place it on the stack
* Finally place the system function address on the stack, send the exploit, and put the program in interactive mode to interact with the shell






