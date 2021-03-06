.. _`setup-configuration`:

Setup & Configuration
====================================================================

.. _`quick-setup`:

Quick Setup
--------------------------------------------------------------------

We assume development or deployment in a MacOS or Linux environment.

As for User:

1. Install Docker 18 (`Ubuntu <https://docs.docker.com/install/linux/docker-ce/ubuntu/>`__, `MacOS <https://docs.docker.com/docker-for-mac/install/>`__)
   and, if required, add your user to ``docker`` group (`Linux <https://docs.docker.com/install/linux/linux-postinstall/>`__).

.. note::

    If you're not a user in the ``docker`` group, you'll instead need ``sudo`` access and prefix every bash command with ``sudo -E``.

2. Install Kubernetes 1.15+ (see :ref:`installing-kubernetes`) if using Kubernetes.

3. Install Python 3.6 such that the ``python`` and ``pip`` commands point to the correct installation of Python 3.6 (see :ref:`installing-python`).

4. pip install singa-auto==0.3.4

5. start the service using : sago
   stop the service using : sastop
   clean the service using : saclean

As for Developer

1. Install Docker 18 (`Ubuntu <https://docs.docker.com/install/linux/docker-ce/ubuntu/>`__, `MacOS <https://docs.docker.com/docker-for-mac/install/>`__)
   and, if required, add your user to ``docker`` group (`Linux <https://docs.docker.com/install/linux/linux-postinstall/>`__).

.. note::

    If you're not a user in the ``docker`` group, you'll instead need ``sudo`` access and prefix every bash command with ``sudo -E``.

2. Install Kubernetes 1.15+ (see :ref:`installing-kubernetes`) if using Kubernetes.

3. Install Python 3.6 such that the ``python`` and ``pip`` commands point to the correct installation of Python 3.6 (see :ref:`installing-python`).

4. Clone the project at https://github.com/nusdbsystem/singa-auto (e.g. with `Git <https://git-scm.com/downloads>`__)

   In file web/src/HTTPconfig.js, there are parameters specifying backend server and port that Web UI interacts with. Developers have to modify the following values to conform with their server setting:

    .. code-block:: shell
    
        const adminHost = '127.0.0.1' # Singa-Auto server address, in str format
        const adminPort = '3000'      # Singa-Auto server port, in str format

        const LocalGateways = {...
          // NOTE: must append '/' at the end!
          singa_auto: "http://127.0.0.1:3000/", # http://<ServerAddress>:<Port>/, in str format
        }

        HTTPconfig.adminHost = `127.0.0.1`  # Singa-Auto server address, in str format
        HTTPconfig.adminPort = `3000`       # Singa-Auto server port, in str format
   By using 127.0.0.1 as Singa-Auto server address, it means Singa-Auto will be deployed on your 'local' machine.

5. If using docker, Setup SINGA-Auto's complete stack with the setup script:

    .. code-block:: shell

        bash scripts/docker_swarm/start.sh

   If using kubernetes, Setup SINGA-Auto's complete stack with the setup script:

    .. code-block:: shell

        bash scripts/kubernetes/start.sh

*SINGA-Auto Admin* and *SINGA-Auto Web Admin* will be available at ``127.0.0.1:3000`` and ``127.0.0.1:3001`` respectively, or the server specified as 'IP_ADRESS' in scripts/docker_swarm/.env.sh or scripts/kubernetes/.env.sh.

If using docker, to destroy SINGA-Auto's complete stack:

    .. code-block:: shell

        bash scripts/docker_swarm/stop.sh

If using kubernetes, to destroy SINGA-Auto's complete stack:

    .. code-block:: shell

        bash scripts/kubernetes/stop.sh

Updating docker images
--------------------------------------------------------------------

    .. code-block:: shell

        bash scripts/kubernetes/build_images.sh

or

    .. code-block:: shell

        bash scripts/docker_swarm/build_images.sh
        bash scripts/push_images.sh

By default, you can read logs of SINGA-Auto Admin & any of SINGA-Auto's workers
in ``./logs`` directory at the root of the project's directory of the master node.


Scaling SINGA-Auto
--------------------------------------------------------------------

SINGA-Auto's default setup runs on a single machine and only runs its workloads on CPUs.

SINGA-Auto's model training workers run in Docker containers that extend the Docker image ``nvidia/cuda:9.0-runtime-ubuntu16.04``,
and are capable of leveraging on `CUDA-Capable GPUs <https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#pre-installation-actions>`__

Scaling SINGA-Auto horizontally and enabling GPU usage involves setting up *Network File System* (*NFS*) at a common path across all nodes,
installing & configuring the default Docker runtime to `nvidia` for each GPU-bearing node. If using docker swarm, putting all these nodes into a single Docker Swarm.
If using kubernetes, putting all these nodes into kubernetes.


.. seealso:: :ref:`architecture`


.. _`GPUs on docker swarm`:
To run SINGA-Auto on multiple machines with GPUs on docker swarm, do the following:


1. If SINGA-Auto is running, stop SINGA-Auto with 

    ::

        bash scripts/docker_swarm/stop.sh


2. Have all nodes `leave any Docker Swarm <https://docs.docker.com/engine/reference/commandline/swarm_leave/>`__ they are in

3. Set up NFS such that the *master node is a NFS host*, *other nodes are NFS clients*, and the master node *shares an ancestor directory
   containing SINGA-Auto's project directory*. `Here are instructions for Ubuntu <https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-16-04>`__

4. All nodes should be in a common network. On the *master node*, change ``DOCKER_SWARM_ADVERTISE_ADDR`` in the project's ``.env.sh`` to the IP address of the master node
   in *the network that your nodes are in*

5. For *each node* (including the master node), ensure the `firewall rules
   allow TCP & UDP traffic on ports 2377, 7946 and 4789
   <https://docs.docker.com/network/overlay/#operations-for-all-overlay-networks>`_

6. For *each node that has GPUs*:

    6.1. `Install NVIDIA drivers <https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html>`__ for CUDA *9.0* or above

    6.2. `Install nvidia-docker2 <https://github.com/NVIDIA/nvidia-docker>`__

    6.3. Set the ``default-runtime`` of Docker to `nvidia` (e.g. `instructions here <https://lukeyeager.github.io/2018/01/22/setting-the-default-docker-runtime-to-nvidia.html>`__)

7. On the *master node*, start SINGA-Auto with 

    ::

        bash scripts/docker_swarm/start.sh

8. For *each worker node*, have the node `join the master node's Docker Swarm <https://docs.docker.com/engine/swarm/join-nodes/>`__

9. On the *master* node, for *each node* (including the master node), configure it with the script:

    ::

        bash scripts/docker_swarm/setup_node.sh

.. _`GPUs on kubernetes`:
To run SINGA-Auto on multiple machines with GPUs on kubernetes, do the following:


1. If SINGA-Auto is running, stop SINGA-Auto with 

    ::

        bash scripts/kubernetes/stop.sh

2. Put all nodes you need in kubernetes cluster, reference to `kubeadm join <https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/>`__

3. Set up NFS such that the *master node is a NFS host*, *other nodes are NFS clients*, and the master node *shares an ancestor directory
   containing SINGA-Auto's project directory*. `Here are instructions for Ubuntu <https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-16-04>`__

4. Change ``KUBERNETES_ADVERTISE_ADDR`` in the project's ``scripts/kubernetes/.env.sh`` to the IP address of the master node
   in *the network that your nodes are in*

5. For *each node that has GPUs*:

    5.1. `Install NVIDIA drivers <https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html>`__ for CUDA *9.0* or above

    5.2. `Install nvidia-docker2 <https://github.com/NVIDIA/nvidia-docker>`__

    5.3. Set the ``default-runtime`` of Docker to `nvidia` (e.g. `instructions here <https://lukeyeager.github.io/2018/01/22/setting-the-default-docker-runtime-to-nvidia.html>`__)

    5.4. Install nvidia-device-plugin, use command "*kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.10/nvidia-device-plugin.yml*" on the *master node*

7. On the *master node*, start SINGA-Auto with ``bash scripts/kubernetes/start.sh``

Exposing SINGA-Auto Publicly
--------------------------------------------------------------------

SINGA-Auto Admin and SINGA-Auto Web Admin runs on the master node.
If using docker swarm, change ``SINGA_AUTO_ADDR`` in ``.env.sh`` to the IP address of the master node
in the network you intend to expose SINGA-Auto in.
If using kubernetes, change ``SINGA_AUTO_ADDR`` in ``scripts/kubernetes/.env.sh`` to the IP address of the master node
in the network you intend to expose SINGA-Auto in.

Example:

::

    export SINGA_AUTO_ADDR=172.28.176.35

Re-deploy SINGA-Auto with step 4, changing Singa-Auto server address to conform. SINGA-Auto Admin and SINGA-Auto Web Admin will be available at that IP address,
over ports 3000 and 3001 (by default), assuming incoming connections to these ports are allowed.

**Before you expose SINGA-Auto to the public,
it is highly recommended to change the master passwords for superadmin, server and the database (located in `.env.sh` as `POSTGRES_PASSWORD`, `APP_SECRET` & `SUPERADMIN_PASSWORD`)**

Reading SINGA-Auto's logs
--------------------------------------------------------------------

By default, you can read logs of SINGA-Auto Admin & any of SINGA-Auto's workers
in ``./logs`` directory at the root of the project's directory of the master node.


Troubleshooting
--------------------------------------------------------------------

Q: There seems to be connectivity issues amongst containers across nodes!

A: `Ensure that containers are able to communicate with one another through the Docker Swarm overlay network <https://docs.docker.com/network/network-tutorial-overlay/#use-an-overlay-network-for-standalone-containers>`__
