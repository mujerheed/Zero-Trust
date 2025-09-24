# Implementation Guide: Setting up your AWS Environment and GitHub Repository
This guide will walk you through the necessary steps to set up your development environment, configure AWS services, and organize your project on GitHub.

## Step 1: Install and Configure the AWS CLI
1. Install the AWS CLI: Follow the official instructions to install the AWS CLI for your operating system.
2. Configure AWS CLI: Open your terminal or command prompt and run the following command:

```bash
aws configure
```

You will be prompted to enter the following information. Use the credentials you obtained when creating your IAM user.
- **AWS Access Key ID:** [Access Key ID]
- **AWS Secret Access Key:** [Secret Access Key]
- **Default region name:** As discussed, choose a region close to your target market (Nigeria). A good choice would be a region in Europe like eu-west-3 (Paris) or Africa like af-south-1 (Cape Town).
- **Default output format:** json

## Step 2: Configure your GitHub Repository
1. **Create a Repository:** Go to your GitHub account and create a new public or private repository for this project.
2. **Clone the Repository:** Clone the empty repository to your local machine using the following command, replacing [Your_Repo_URL] with your repository's URL:

```bash
git clone [Your_Repo_URL]
```

3. **Create Project Structure:** Navigate into the cloned directory and create the following file and folder structure. This modular approach will keep your codebase organized and scalable.
```
/
├── docs/ (documentations)
│   ├── Project_Proposal.md
│   ├── Implementation_Guide.md
│   ├── System_Architecture.md
├── backend/
│   ├── lambda_functions/
│   ├── templates/ (for infrastructure as code files)
├── frontend/ (Ui for Vendors/CEO)
├── .gitignore
├── README.md
├── 
```

4. **Add Initial Files and Push:** Copy the _README.md_ and _Project_Proposal.md_ files we created earlier into the root directory. Add and commit these files to your repository.

```bash
git add .
git commit -m "Initial project setup with README and proposal"
git push -u origin main
```

## Step 3: Create the DynamoDB Table
The otp_generator.py Lambda function requires a DynamoDB table to store the generated OTPs. You can create this table directly from the AWS Management Console.
1. Log in to the AWS Management Console: Go to the AWS console.
2. Navigate to DynamoDB: In the search bar, type "DynamoDB" and select the service.
3. Create a New Table: Click the "Create table" button.
- Table name: Use a descriptive name like zero-trust-otps or the name you prefer. This is the name you will set as an environment variable in your Lambda function later.
- Partition key: Enter identifier. This will be the unique key for each OTP entry (e.g., the phone number or email of the buyer/vendor). Select String for the data type.
- Sort key: This is not required for this table.
- Table settings: Leave the default settings for now (e.g., On-demand capacity mode).
4. Add a Time-to-Live (TTL) Attribute: This is a crucial security feature that automatically deletes old OTPs, preventing replay attacks.
- Under the "Table details" section, go to the "Additional settings" tab.
- Click "Enable" under the "Time-to-Live (TTL)" section.
- Choose a TTL attribute name. We will use expiresAt. This is the same attribute name we used in the Python code, so the table and the Lambda function will work together seamlessly.
5. Finalize Table Creation: Review your settings and click "Create table."
Once the table is created, you have successfully set up the foundational infrastructure for our OTP generation module.