#!/bin/bash

current_dir=$(pwd)

sudo cp -ar "$current_dir" /usr/lib/

echo -e '#!/bin/bash\npython /usr/lib/bible/main.py' | sudo tee -a /usr/bin/bible > /dev/null
sudo chmod +x /usr/bin/bible

sudo cp /usr/lib/bible/bible.desktop /usr/share/applications
sudo chmod +x /usr/share/applications/bible.desktop

echo "Installation complete."
