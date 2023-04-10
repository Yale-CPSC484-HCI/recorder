# Setting up the recorder on the Zoo

The following steps describe how to setup the recorder utility under your account on the [Zoo](https://zoo.cs.yale.edu/newzoo/).
For more information about the usage of the recorder, refer to the [main readme](../README.md).

 1. Login to the Zoo (either in person or over SSH).

    ```
    $ ssh <netid>@node.zoo.cs.yale.edu
    ```

    > Note that you can setup the project on any node of the Zoo, and it will be available on any Zoo machine.

 2. Checkout pyenv to a local directory: [https://github.com/pyenv/pyenv#basic-github-checkout](https://github.com/pyenv/pyenv#basic-github-checkout)

    ```
    $ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    ```

 3. Put pyenv on the PATH: [https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

    `bash` is the default shell on the Zoo machines, so you should run the commands in the `bash` subsection:

    ```
    $ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    $ echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    $ echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    ```

    To apply the changes to your current shell session, run

    ```
    $ source ~/.bashrc
    ```

    And then check that pyenv is on your PATH:

    ```
    $ pyenv --version
    pyenv <version number should appear here>
    ```

    If the version number doesn't appear, you should verify that the file `.bashrc` has exports the environment variables indicated by the pyenv readme, then re-login to the Zoo.

 4. Install pipenv:

    ```
    $ pip install pipenv
    ```

    To check that pipenv is installed, you can run:

    ```
    $ pipenv --version
    pipenv, version <version number should appear here>
    ```

 5. Setup SSH Private Key authentication to GitHub (follow this tutorial on GitHub)

    To check that your SSH key is added, you can run:

    ```
    $ ssh -T git@github.com
    Hi <GitHub username>! You've successfully authenticated, but GitHub does not provide shell access
    ```

 6. Clone repository (make sure to clone with SSH!).

    ```
    $ cd ~
    $ git clone git@github.com:Yale-CPSC484-HCI/recorder.git
    ```

 7. Configure virtual environment

    ```
    $ cd ~/recorder
    $ pipenv install
    ```

    This step should install the dependencies enumerated in `Pipfile`.
    You should see a lot of console output that sets up a new virtual environment and installs the dependencies.

 8. Running the recorder

    ```
    $ pipenv run python src/main.py --data-path data/sample --mode play
    ```

    > Note that if you are connecting to the Zoo via SSH, you should follow Step 9 below. Otherwise, move to Step 10.

 9. **Port forwarding (if you are connecting via SSH).**
    If you are connecting to the Zoo via SSH, you will need to enable [port forwarding](https://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding) in order to access the WebSocket that exposes Kinect body tracking data.

    To invoke port forwarding, start a new SSH session based on the following form:

    ```
    $ ssh -L 4040:localhost:4444 <your netid>@node.zoo.cs.yale.edu
    ```

    This command forwards the port 4444 from the Zoo to your local machine's port 4040.
    Note that you might need to change the port 4444 if it is already in use.
    In this case, you will also need to change the port used by the recorder tool:

    ```
    // on your local machine
    $ ssh -L 4040:localhost:1414 netid@node.zoo.cs.yale.edu

    // on the Zoo
    $ cd recorder
    $ pipenv run python src/main.py --data-path data/sample --mode play --local-port 1414
    ```


10. Viewing the data in a web browser:

    Once you've started port forwarding, you can open a web browser on your machine to http://127.0.0.1:4444/.
    And the data should be visible in your web browser!

    > Note that if you are using port forwarding, you should change 4444 to the local port, e.g. http://127.0.0.1:4040

11. If your project doesn't require another Python virtual environment, you can develop your website locally by substituting `http://127.0.0.1:<appropriate port here>` for the websocket.
    Then, you can continue to edit your HTML, CSS and JavaScript files locally.
