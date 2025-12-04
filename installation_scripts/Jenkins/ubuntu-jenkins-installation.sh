# https://www.jenkins.io/doc/book/installing/linux/#debianubuntu

######################################################
# ======= Install Java 21 (pre-requisite) =======
######################################################
echo "Installing Java 21..."
sudo apt update
sudo apt install fontconfig openjdk-21-jre -y
java -version

######################################################
# ======= Add Jenkins Repository and Key =======
######################################################
echo "Adding Jenkins Repository and Key..."
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

######################################################
# ======= Install Jenkins ======= 
######################################################
echo "Installing Jenkins..."
sudo apt update
sudo apt install jenkins -y

######################################################
# ======= Start and Enable Jenkins Service =======
######################################################
echo "Starting and Enabling Jenkins Service..."
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo systemctl status jenkins
######################################################
# ======= Display Initial Admin Password =======
######################################################
echo "Initial Admin Password for Jenkins:"
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
echo "========================================"======================
echo "You can access Jenkins at: http://<your_server_ip>:8080"
echo "========================================"======================