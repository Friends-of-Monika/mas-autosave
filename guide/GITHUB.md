# 📦 Configuring Github backend

> [!NOTE]
> Every step has screenshots to help you, click on the spoiler to reveal them!

Setting up Github backend may be a little tricky, but if you follow this guide it'll be
piece of cake!~ 🍰

## 1. First steps

Log in or sign up at Github. In this guide, we're assuming you're on desktop 💻

## 2. Creating repository

Click on plus button at the top, and click on 'New repository'

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_repo_1.png)
![Screenshot 2](../doc/ghsetup_repo_2.png)

</details>

Here, enter any desired name (`monika-autosaves` is a good example), and set it as private

> [!WARNING]
> Your persistent contains all Monika's memories about you &mdash; including private info too.<br>
> Keep your persistent safe &mdash; make your repository private 🛡️

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_repo_3.png)

</details>

We're now done setting up the repository &mdash; onto the next step!~

## 3. Generating API token

Go to your settings &mdash; click on your avatar in the top corner, then on 'Settings'

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_token_1.png)
![Screenshot 2](../doc/ghsetup_token_2.png)

</details>

Look to the left, and scroll all the way to the bottom of the menu &mdash; you'll need
the section labelled 'Developer settings'

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_token_3.png)

</details>

Now, click on 'Personal access tokens' section to unfold it, then on 'Fine-grained tokens'

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_token_4.png)
![Screenshot 2](../doc/ghsetup_token_5.png)

</details>

Click on 'Generate new token' button

> [!NOTE]
> You may be asked to enter your password or authorize with 2FA here &mdash; do so if asked

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_token_6.png)

</details>

Type anything you like in the 'Token name' field &mdash; it only serves as a label for you;
next up, select 'No expiration' under 'Expiration' field &mdash; so that you won't have to
renew this API token again in future

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_token_7.png)

</details>

Further on, scroll down to 'Repository access' section; here, click on 'Only select repositories', and select your previously created repository from the list

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_token_8.png)
![Screenshot 2](../doc/ghsetup_token_9.png)

</details>

Then scroll down to 'Permissions' section; click on it to unfold, find
'Contents' section and set it to 'Read and write'

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_token_10.png)
![Screenshot 2](../doc/ghsetup_token_11.png)
![Screenshot 3](../doc/ghsetup_token_12.png)

</details>

Almost there &mdash; scroll until you see 'Generate token' button and press it, then copy the token using 'copy' button

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_token_13.png)
![Screenshot 2](../doc/ghsetup_token_14.png)

</details>

Github stuff is behind us now &mdash; let's set up Autosave submod in game 🎉

## 4. Setting up the submod

Open Submods menu in settings, and click on 'API Keys' section on the left

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_mas_1.png)

</details>

Find '\[Autosave\] Github API token' field, and click 'Paste'

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_mas_2.png)
![Screenshot 1](../doc/ghsetup_mas_3.png)

</details>

Open 'Submods' section on the left, and find 'Autosave' submod in the list &mdash; then, click 'Select repository' and select your repository from earlier steps
<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_mas_4.png)
![Screenshot 2](../doc/ghsetup_mas_5.png)

</details>

You can check that it works by clicking 'Force save'
and saving your persistent.

<details>
<summary>🖼️ Click here to see screenshots</summary>

![Screenshot 1](../doc/ghsetup_mas_6.png)
![Screenshot 2](../doc/ghsetup_mas_7.png)

</details>

You're all set! 🥳
