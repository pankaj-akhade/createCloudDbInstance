#!/usr/bin/python
from argparse import ArgumentParser
from subprocess import call
import shutil
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
        f.write('project = "' + str(args.project) + '"\n')
        f.write('region = "' + str(args.region) + '"\n')
        f.write('cloudsqlname = "' + str(args.cloudsqlname) + '"\n')
        if args.tier:
            var = '"' + args.tier + '"'
            f.write('tier = ' + var + '\n')
        if args.dbversion:
            var = '"' + args.dbversion + '"'
            f.write('dbversion = ' + var + '\n')

if(__name__ == '__main__'):
    ######Parsing command line aurguements######
    parser = ArgumentParser(description='This script is used to create Cloud SQL in GCP')
    parser.add_argument('--project', required=True, help='Your GCP Project')
    parser.add_argument('--region', required=True, help='Region [eg. us-east1]')
    parser.add_argument('--cloudsqlname', required=True, help='Enter GCP cloud SQL name')
    parser.add_argument('--tier', required=False, help='DB instance type[default: db-n1-standard-1]')
    parser.add_argument('--dbversion', required=False, help='DB instance version[default: MYSQL_5_7]')
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--create', action='store_true', help='Create resources')
    action.add_argument('--delete', action='store_true', help='Delete resources')
    contype = parser.add_mutually_exclusive_group(required=True)
    contype.add_argument('--private', action='store_true', help='Private SQL connection')
    contype.add_argument('--public', action='store_true', help='Public SQL connection')
    args = parser.parse_args()

    ##Initialising Terraform object
    if args.create:
        if args.private:
            filename = 'main.tf' + '_privatecon'
            shutil.copy2(filename, 'main.tf')
        elif args.public:
            filename = 'main.tf' + '_publiccon'
            shutil.copy2(filename, 'main.tf')
        ##Set tf vars
        set_tf_vars(args)
        ##Initialising Terraform
        tf_init()
        ##Creating resources
        tf_apply()
    elif args.delete:
        ##Destroying resources
        tf_destroy()
