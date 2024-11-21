echo "updating and upgrading --------------------------------------------------"
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip -y

echo "clearing out old files --------------------------------------------------"
sudo rm -rf /var/www/
sudo mkdir -p /var/www

echo "cloning the repository --------------------------------------------------"
cd /var/www/
sudo git clone https://github.com/Nordsword3m/rbnlp.git
cd rbnlp
sudo git submodule update --init --recursive

echo "setting up virtual environment --------------------------------------------------"
sudo apt-get install python3-venv -y

echo "creating virtual environment --------------------------------------------------"
sudo python3 -m venv /var/www/rbnlp/venv

echo "installing requirements --------------------------------------------------"
sudo /var/www/rbnlp/venv/bin/python3 -m pip install -r requirements.txt 

# Stop all screens
echo "stopping all screens --------------------------------------------------"
for session in $(screen -ls | grep -oP '\d+\.\w+' | cut -d. -f1); do screen -S "${session}" -X quit; done

# Start the server
echo "starting server --------------------------------------------------"
sudo screen -d -m /var/www/rbnlp/venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 80
echo "Server started --------------------------------------------------"