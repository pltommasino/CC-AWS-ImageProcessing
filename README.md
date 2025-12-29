# Project Overview ☁️

This repository contains the complete implementation of a cloud-based system deployed on AWS, including the application architecture, performance evaluation, and supporting documentation.

## Architecture Application 📐

<img width="1079" height="696" alt="arch" src="https://github.com/user-attachments/assets/01d45b9f-2ed4-4020-b76f-c137b7c8cec1" />

## Repository Structure 📂

- **`application/`** 🏗️  

  This folder contains everything related to the main system architecture, as illustrated in the architectural diagram provided in the documentation. It includes all components required to deploy, configure, and run the full end-to-end application on AWS.

- **`locust/`** ⚙️  

  This folder contains all resources related to the performance evaluation of the system.  
  The performance tests are executed on a separate and simplified architecture, different from the main application architecture.

- **`pdf/`** 📄  

  This folder contains the performance analysis paper, detailing the methodology, experimental setup, and results of the performance evaluation. It also includes a step-by-step guide explaining how to build and deploy the application without the Locust-based performance testing infrastructure.

## Performance Evaluation Rationale 🚀

The performance evaluation was deliberately conducted using a different architecture from the production-like system. This design choice was made to avoid bottlenecks, interference, and unwanted noise introduced by non-essential components. Rather than evaluating the entire architecture, the analysis focuses exclusively on the core component of the system, the **ConvertBW**.

By isolating this critical service, we were able to: obtain more reliable and reproducible performance measurements, accurately analyze scalability and throughput and prevent results from being biased by auxiliary services or infrastructure overhead. This approach enables a cleaner, more controlled, and more meaningful assessment of the system’s computational core.
