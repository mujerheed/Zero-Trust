# <center>Zero Trust Security System for Informal E-Commerce</center>

This project proposes and implements a Zero Trust Security System designed to address fraud and security vulnerabilities within Nigeria's informal e-commerce sector, which primarily operates on social media platforms like WhatsApp and Instagram.
The project's core principle is "never trust, always verify," replacing the current implicit trust model with a verifiable and auditable framework.

## Key Features
- **Enhanced OTP-Based Verification:** Uses alphanumeric One-Time Passcodes with special characters for both buyer/vendor and CEO verification, significantly increasing security.

- **Hybrid Receipt Handling:** Encrypts and securely stores proof of payment in the cloud. Receipts are automatically checked for authenticity, but if flagged as suspicious, they are routed to the vendor for manual re-investigation and approval, accommodating real-world scenarios.

- **Role-Based Access Control (RBAC):** Differentiates permissions between buyers, vendors, and administrators to enforce the principle of least privilege.

- **High-Value Transaction Escalation:** Triggers a multi-level approval process for transactions exceeding a specific financial threshold.

- **Zero-App Integration:** Designed to work seamlessly with existing communication channels, eliminating the need for buyers to download a new application.

- **Automated Audit Logging:** Maintains a comprehensive log of all transactions and security-related events for accountability.

## Getting Started
This project is a cloud-native, serverless application built on AWS. To get started, follow the steps in the _Implementation_Guide.md_ to configure your AWS Command Line Interface (CLI) and set up the project on GitHub.

## Technology Stack
- **Cloud Platform:** AWS (Lambda, DynamoDB, S3, Cognito, SNS)
- **Programming Language:** Python
- **Frontend:** HTML/React

## Limitations
1. Manual Receipt Verification: Currently, receipt verification is manual. AI-based fraud detection is planned for a future phase to fully automate the receipt detection and direct Integration with ban APIs.

2. OTP Dependency on Network: The system relies on a stable network connection for OTP delivery and all cloud-based functions.

3. Limited Multi-Channel Support: Initially, the system is limited to WhatsApp, Instagram, and SMS for buyer interactions.

4. Human Error in Vendor Checks: Manual checks are susceptible to human error.

5. No Offline Support: The system relies entirely on cloud connectivity.

6. Scalability Constraints: Initial deployment is targeted at small-to-medium vendors; large-scale scaling may require additional optimizations and infrastructure.

## Project Status
This project is currently in the initial implementation phase, focusing on **Module 1: Foundational Services & OTP Generation.**