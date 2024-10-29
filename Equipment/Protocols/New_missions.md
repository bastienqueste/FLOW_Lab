# List of software used in preparation for fieldwork

* Ensure you have a functioning windows installation (standalone or through a VM)
* Teraterm
* Ruskin (RBR - https://rbr-global.com/products/software/) for Legato and Coda
* UCI (Seabird - https://www.seabird.com/uci-2-0-4) for SUNA
* AROD-FT (JFE - in this repo folder) for the AROD-FT oxygen sensor
* Zissou Premium (Rockland - contact Bastien) for the MR-1000G
* MIDAS (Nortek - https://gunet-my.sharepoint.com/:u:/r/personal/bastien_queste_gu_se/Documents/Bifogade%20filer/NortekMIDAS_V1.37_R4421_21-01-05-07.zip?csf=1&web=1&e=wbSpHd) for the Nortek
* VPN for Oman


# Protocols
## VOTO preparation documents (TODO: copy documents to repo)
* Compass calibr, testing release and argo tag: https://drive.google.com/file/d/10UlJtEKZ7Q_g5udiAcJv6sK5OFUpjk_A/view?usp=sharing
* Data download: https://drive.google.com/file/d/1vRQgxeT8gixs00R-1oQ1K8Kx1lFt0nTh/view?usp=sharing

## To do list for pilot
* Set up mission plan on Glimpse for all gliders.
* Set up MR-1000G ISDP file; send to field team for review and upload.
* Set up sea.cfg, sea.msn and seapayload.cfg; send to field team for review and upload.

## To do list for field team (last update: Oman 2024 missions)
* Pick up tails and serial cable to make DIY cable.
* Test satellite phone
* Test argo tag
* Sensors:
  * CTD  (before SIM dives)
    * Antifouling (1 pea sized lump of high adhesive silicone grease with 1 drop of spicy juice, thoroughly mixed, use gloves, spread super thin on the top of the sensor frame). Maybe do the same for common areas of growth (screw heads).
  * ADCP  (before SIM dives)
    * compass calibrate
    * Antifouling (see above)
  * O2 (coda AND arod)  (before SIM dives)
    * Calibrate in sodium sulfite.
    * Calibrate in 100% water.
    * Use AROD software (slack) and Ruskin.
    * https://oceangliderscommunity.github.io/Oxygen_SOP/README.html# 
  * MR (before SIM dives)
    * MR config (ISDP file)
    * Bench test
    * Test probes:
      * 0.75nF for shear.
      * 2kOhm for microT
      * Note: It is important to compare with the original value, older probes were calibrated on 1.0 nF, and the 15% drop should be calculated on that value. Do it before and after every deployment, and keep track!
  * SUNA (before SIM dives)
    * Collect data with distilled water water (wrap around with electrical tape, poke hole, fill with distilled water) during SIM dives.
    * Use UCI software (Section 2.3 "Update the reference value" in the UCI manual). Note that this requires switching the Operational Mode to continuous, make sure ot return to original setting after (can't recall what it is right now - BYQ)
    * https://oceangliderscommunity.github.io/Nitrate_SOP/README.html#
    * Back up SUNA settings before making changes.
  * Chl and optical backscatter (*during* SIM dives)
    * Estimate dark counts - tape it for a couple of the sim dives (no tape glue on surface, tape something thick like several sheets of black paper over the top of it)

* Glider
  * Upload seapayload.cfg, sea.cfg, sea.msn
  * Compass calibration
  * RunTester 
    * test max and min of bladder, angular and linear
    * Vacuum
    * Test release device
    * Simulation dives (mode 3) !change mission numbers!
  * Download data - Verify data integrity  -- Delete files:)
  * Set up for transport (motors to neutral) and mission num +1 and mission mode 0

* Charge!

## Packing list for deployment (let's try take everything..)
* Buoy
* Ethernet glider, MR cable, ADCP cable
* Sat phone

## Deployment
* Sensor caps off
* Argo tag on
* Check coms with land
* Buoy
* Check all runTesters - energy, vacuum, and motors!


