# For runing MailHog locally

This app by default uses MailHog as mail server

### Installation

#### MacOS

```bash
brew update && brew install mailhog
```

Then, start MailHog by running `mailhog` in the command line.

#### Debian / Ubuntu Go < v1.18

```bash
sudo apt-get -y install golang-go
go get github.com/mailhog/MailHog
```

#### Go >= v1.17 (Debian Bookworm)

```bash
sudo apt-get -y install golang-go
go install github.com/mailhog/MailHog@latest
```

Then, start MailHog by running `/path/to/MailHog` in the command line.

E.g. the path to Go's bin files on Ubuntu is `~/go/bin/`, so to start the MailHog run:

```bash
~/go/bin/MailHog
```
