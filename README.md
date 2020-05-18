# createCloudDbInstances
-------------------------------------------------------------------------------

python createDbInstance.py --help
usage: createDbInstance.py [-h] --cloud CLOUD --dbType DBTYPE --engine ENGINE
                           [--vpcId VPCID] [--publicAccess] [--skipFinalSnap]
                           [--project PROJECT] --region REGION [--user USER]
                           [--password PASSWORD] --dbname DBNAME [--tier TIER]
                           [--storageType STORAGETYPE]
                           [--allocatedStorage ALLOCATEDSTORAGE]
                           [--profile PROFILE] [--dbversion DBVERSION]
                           (--create | --delete) [--private | --public]

This script is used to spin up database instances in AWS/GCP

optional arguments:
  -h, --help            show this help message and exit
  --cloud CLOUD         Cloud vendor eg. aws/gcp
  --dbType DBTYPE       dbType i.e. oracle/mysql/mssql
  --engine ENGINE       db engine type i.e. oracle/mysql/mssql
  --vpcId VPCID         Required for AWS
  --publicAccess        Required for AWS [Public/Private]
  --skipFinalSnap       [Optional]Required for AWS
  --project PROJECT     Your GCP Project
  --region REGION       Region [eg. us-east1]
  --user USER           db username Required for AWS
  --password PASSWORD   db password Required for AWS
  --dbname DBNAME       Enter db name
  --tier TIER           DB instance type
  --storageType STORAGETYPE
                        db storage type:gp2/ipos
  --allocatedStorage ALLOCATEDSTORAGE
                        Allocate storage to db instance [default:20]
  --profile PROFILE     [Optional] Required for AWS[default: default]
  --dbversion DBVERSION
                        DB instance version
  --create              Create resources
  --delete              Delete resources
  --private             Private SQL connection
  --public              Public SQL connection
  -------------------------------------------------------------------------------
  
  GCP:
  python createDbInstance.py --cloud gcp --dbType <mysql|mssql> --engine <mysql|mssql> --region <region> --dbname <dbName> --tier <instance-class> --dbversion <dbversion> --create --private --project <Project>
  
  AWS:
  python createDbInstance.py --cloud aws --dbType <mssql|oracle> --engine <sqlserver-se|oracle-se|etc.> --region <region> --dbname <dbName> --vpcId <vpc-id> --user <user> --password <password> --tier <instance-class> --dbversion <dbversion> --publicAccess --create
