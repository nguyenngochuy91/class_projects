# Downloading movies file from Standford website
## Installation
1. Download python3.4 here [Python 3.4](https://www.python.org/download/releases/3.4.0/)
2. Download beautifulsoup here [Beautifulsoup 4](https://www.crummy.com/software/BeautifulSoup/) for web/screen scraping
3. Download flash player standalone here [Flash Player Standalone](https://www.adobe.com/support/flashplayer/debug_downloads.html) to watch the .swf file
4. User can either use github interface download or type the following command in command line:
```bash
git clone https://github.com/nguyenngochuy91/class_projects/new/master/CS_569_ProteinStructure
```
The script was written in python3

## Usage
* Step 1: Create a directory to store the movies, name it /movie/ and copy the program **“get_talklet.py”** into /movie/
  1. Type ```bash ./get_talklet.py -h ``` for user choices 
  2. The choice right now is which lecture to download, which is indicated after -l options. For example, if you want to download lecture 2:
  ```bash ./get_talklet.py -l 2```
  3. The program should automatically create a directory lecture 2 and download all the movies into that folder. While doing it, it will keep
  opening new tab in your web browser (this is needed since the movie file is in swf, and it must be loaded before we can actualy curl it to download)
  4. After it stops opening new tab, you can close the web browser and enjoy the movies hopefully (lol)
 ( I will work on how to automatically kill the process of the browser, probably just use os package to find the uid of the thread and kill it)
  5. Use flash player standalone you download to watch, I am working on a merger for all, but it leads me to nowhere right now :(.
