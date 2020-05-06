#!/usr/bin/python
from argparse import ArgumentParser
from subprocess import call
import shutil
import os
from termcolor import colored
####Terraform python package does not provide auto-approve functionality. So we are using terraform commands directly.

def tf_apply():
    call("terraform apply -auto-approve", shell=True)

def tf_init():
    call("terraform init", shell=True)

def tf_destroy():
    call("terraform destroy -auto-approve", shell=True)

def set_tf_vars(args):
    with open('terraform.tfvars', 'w') as f:
        f.write('')
    with open('terraform.tfvars', 'a') as f:
        for key, value in args.__dict__.items():
            if value is not None and key not in ["private", "public", "create", "delete", "dbType", "cloud"]:
                if args.cloud == 'gcp' and key in ["publicAccess", "skipFinalSnap", "engine"]:
                    continue
                if isinstance(value, bool) :
                    f.write('{} = {}\n'.format(str(key), str(value).lower()))
                    continue
                f.write('{} = "{}"\n'.format(str(key), str(value)))

if(__name__ == '__main__'):
    ######Parsing command line aurguements######
    parser = ArgumentParser(description='This script is used to spin up database instances in AWS/GCP')
    parser.add_argument('--cloud', required=True, help='Cloud vendor eg. aws/gcp')
    parser.add_argument('--dbType', required=True, help='dbType i.e. oracle/mysql/mssql')
    parser.add_argument('--engine', required=True, help='db engine type i.e. oracle/mysql/mssql')
    parser.add_argument('--vpcId', required=False, help='Required for AWS')
    parser.add_argument('--publicAccess', action='store_true', required=False, help='Required for AWS [Public/Private]')
    parser.add_argument('--skipFinalSnap', action='store_true', required=False, help='[Optional]Required for AWS')
    parser.add_argument('--project', required=False, help='Your GCP Project')
    parser.add_argument('--region', required=True, help='Region [eg. us-east1]')
    parser.add_argument('--user', required=False, help='db username Required for AWS')
    parser.add_argument('--password', required=False, help='db password Required for AWS')
    parser.add_argument('--dbname', required=True, help='Enter db name')
    parser.add_argument('--tier', required=False, help='DB instance type')
    parser.add_argument('--storageType', required=False, help='db storage type:gp2/ipos')
    parser.add_argument('--allocatedStorage', required=False, help='Allocate storage to db instance [default:20]')
    parser.add_argument('--profile', required=False, help='[Optional] Required for AWS[default: default]')
    parser.add_argument('--dbversion', required=False, help='DB instance version')
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--create', action='store_true', help='Create resources')
    action.add_argument('--delete', action='store_true', help='Delete resources')
    contype = parser.add_mutually_exclusive_group(required=False)
    contype.add_argument('--private', action='store_true', help='Private SQL connection')
    contype.add_argument('--public', action='store_true', help='Public SQL connection')
    args = parser.parse_args()

    curr_dir = os.getcwd()
    if(args.cloud == 'aws' or args.cloud == 'gcp'):
        cloud_dir = os.path.join(curr_dir, args.cloud)
    else:
        print(colored('You must provide valid cloud provider. Only aws and gcp are supported.','red'))
        exit(1)

    tf_dir = os.path.join(cloud_dir, args.engine)
    gcpDbTfFile = None
    if args.private:
        tf_dir = os.path.join(tf_dir, 'private')
        gcpDbTfFile = args.dbType + '.private.tf'
    elif args.public:
        tf_dir = os.path.join(tf_dir, 'public')
        gcpDbTfFile = args.dbType + '.public.tf'
    if(not os.path.exists(tf_dir)):
        os.makedirs(tf_dir)


    ##Initialising Terraform object
    if args.create:
        if args.cloud == 'gcp':
            if (not args.private and not args.public) or not args.project:
                print(colored('You must provide valid connection method[--public/--private] and you must provide project name[--project]','red'))
                exit(1)
            shutil.copy2(gcpDbTfFile, tf_dir)
            shutil.copy2('account.json', tf_dir)
        else:
            shutil.copy2(args.dbType + '.tf', tf_dir)
        shutil.copy2('terraform.tfvars', tf_dir)
        os.chdir(tf_dir)
        ##Set tf vars
        set_tf_vars(args)
        ##Initialising Terraform
        tf_init()
        ##Creating resources
        tf_apply()
    elif args.delete:
        os.chdir(tf_dir)
        ##Destroying resources
        tf_destroy()
        if os.path.exists('account.json'):
            os.remove('account.json')