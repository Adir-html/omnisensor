# omnisensor
... And by Omnisensor, I mean exclusively temperature.
My home automation system code built for Rapsberry Pi Pico and Nano.

## Pico instructions
Use Thonny to upload the code to the Pico.
Set each node to have a different Pico ID before flashing.

## Nano instructions
### Scanner
The scanner gathers all of the beacons from the nodes and dumps the latest into a .csv in the webroot.
Use `sudo nohup python scanner.py &` to run the scanner.

### Sorter
The sorter reads the .csv written by the scanner and outputs the most recent Voltage and Temerature from each node into another .csv.
Use a 5 minute cron job to run the sorter (see crontab).

### Web interface
The web interface is written entirely by ChatGPT 3.5. The web interface is fronted by nginx in my setup.