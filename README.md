# AWS Image Processing Project

### 🛜 Enable HTTPS in Live Server on VS Code

This guide explains how to serve your local HTML files over **HTTPS** using the **Live Server** extension in Visual Studio Code:

1.  Open **the exact folder that contains the HTML file** you want to expose through HTTPS on localhost. Live Server reads its configuration only from the root of the opened folder, so this step is crucial.

2. Inside your project folder, run:
```bash
mkdir https
```
After:
```bash
cd https
```
This directory will store the private key and the certificate needed for HTTPS.

3. Run the following command:
```bash
openssl genrsa -aes256 -out localhost.key 2048
```
This command generates a 2048-bit RSA private key, encrypted via AES-256. You will be asked to enter a **passphrase** twice. Remember it, because you will need it in the configuration file.

4. Run:
```bash
openssl req -days 3650 -new -newkey rsa:2048 -key localhost.key -x509 -out localhost.pem
```
This command generates a **self-signed certificate** using the private key from step 3 and sets a validity of **10 years**. You will be asked for several pieces of information (Country, City, Organization, etc.). You can simply press **Enter** for all fields.

5. Go back to your project root:
```bash
cd ..
```
After create the `.vscode` directory:
```bash
mkdir .vscode
```
Enter in the new directory:
```bash
cd .vscode
```
This directory will contain the local configuration for Live Server.

6. Run:
```bash
touch settings.json
```

7. Open the newly created `settings.json` file and insert:
```bash
{
    "liveServer.settings.https": {
        "enable": true,
        "cert": "/entire_path/to/localhost.pem",
        "key": "/entire_path/to/localhost.key",
        "passphrase": "12345"
    }
}
```
Replace **`/entire_path/to/localhost.pem`** with the **full absolute path** to the certificate file. Replace **`/entire_path/to/localhost.key`** with the **full absolute path** to the private key. Replace **`12345`** with the **exact passphrase** you used in step 3.

8. Open your HTML file in VS Code, right-click **Open with Live Server**. Your project will now be served over **HTTPS**.