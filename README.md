# XYZ-Logistics
Django sample project

There are several branches to the logistic company XYZ, i.e, Root and Node_1 to Node_9. Root is the head branch.

Every node has a manager. i.e, Root has root and Node_x has manager_x. Funds can be transferred from a node to the other but only if they are parent-child nodes. Fund transfer can be done only by manager of the Root branch. It is assumed that Root already has a fixed amount of fund.

There are two types of groups for managers `root_users` and `node_managers`. Only managers in the `root_users` group can transfer the fund. Password for all the managers is `laptop1234`.

URLs
1. http://127.0.0.1:8000/
2. http://127.0.0.1:8000/admin

APIS
1. http://127.0.0.1:8000/api/v1/node/ - list all the nodes
2. http://127.0.0.1:8000/api/v1/node/1/ - details of node with id = 1
3. http://127.0.0.1:8000/api/v1/transaction/ - lists all the transactions
4. http://127.0.0.1:8000/api/v1/transaction/1/ - details of transaction with id = 1

Basic Authentication is enabled with username and password

