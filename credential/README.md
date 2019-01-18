# Google-Cloud-Note


### How to Get a Credential Json
- select `IAM & admin` from hamburger menu
- select `service account`
-   -   click `create service account`
-   -   fill the name and description
-   -   click `create`
-   -   fill the role
-   -   click `continue`
-   -   click `create key`
-   -   `done`

### How to Execute Json Credential Key
-   `export GOOGLE_APPLICATION_CREDENTIALS=<path to your .json key>`
-   `nano ~/.profilee` then add this: `export GOOGLE_APPLICATION_CREDENTIALS=<path to your .json key>` (optional if step 1 fail)
-   `source ~/.bashrc` (optional if step 1 fail)
