# Home Internet Monitor
_Monitor your home internet speeds in a (somewhat) simple way!_

Are you curious about how well your internet connection is working? Do you think that you could be getting less-than-advertised speeds from your ISP and want a way to prove it? Well, maybe this utility will help.

Here's how this works:
- A Python3 script runs tests using the SpeedTest library and collects the data from the test.
- A MySQL/MariaDB backend database is used to house the data for each test.
- A Grafana instance with a custom dashboard will query MySQL/MariaDB and display the metrics in an easy-to-digest fashion.

The Python3 script collects the following from the test:
- The "server" where the test was run, which is actually the City where the server resides.
- The URL for the SpeedTest server.
- The Download and Upload speeds for the test.
- The Ping for the test.
- The Latitude and Longitude of the server location.

I've been running this on a Raspberry Pi 4B, but this can run just about anywhere you'd like it to. In regards to storage over a 30 day period with tests every 5 minutes, it comes down to a database size of 1.1MB. 

## Setup

1. Clone the repo to your local machine.

2. Install the necessary Python packages via the `requirements.txt` file.
```
~$ pip3 install -r requirements.txt
```

3. Setup MySQL or MariaDB
   - Install MySQL or MariaDB:
_Note: As of this writing, I am running MariaDB 10.5.23-MariaDB-0+deb11u1 on my Raspberry Pi, but there isn't a version dependency, so pick the latest._
```
~$ [apt/yum/dnf] install mysql-server
# -OR-
~$ [apt/yum/dnf] install mariadb-server
```
    - Use the `stMetrics_tableSetup.sql` file to create the needed database & table:
_Open and modify the file first before running this as there is a generic password set in the file for the database user for reference purposes_
```
mysql> source /path/to/stMetrics_tableSetup.sql
```

4. Create a .cnf file to house your database login credentials for the script to read.

```
~$ vim /etc/mysql/.metric.cnf

# Within the file:

[client]
host=localhost
database=stMetrics
user=metric
password=(Password you set in the .sql file)

:wq # to save and quit file
```

5. Set up the Grafana repository and download Grafana
Follow the steps on the [official Grafana site](https://grafana.com/docs/grafana/latest/setup-grafana/installation/) to set up based on your distro.

6. Launch your Grafana instance and import the Network Monitoring JSON to pull in the default dashboard.
   - Select the hamburger menu -> Dashboards
   - In the top right, select New -> Import
   - Select the "Upload dashboard JSON file" option or drag-and-drop the file from your file explorer. 
   - Select OK on the next screen and the Dashboard should appear.

7. Run the Python script to collect your first set of data. Then, set it to run automatically via a cron so it gathers data regularly.
   - I have mine set to be a bit more aggressive and run every 5 minutes, but you can be more aggressive -or- conservative and run at whichever interval you prefer. 
