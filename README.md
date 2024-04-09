# All In One Rust Pterodactyl Egg

This egg includes all of the Carbon builds, as well as a build for Oxide. This enables you to easily test the difference in performance between Oxide and Carbon. It also includes some great QoL features!

The main functionality of this egg is to have the ability to switch seamlessly between all Carbon builds, Oxide, and Vanilla. If you launch the egg with an Oxide build, you can then switch right on over to Carbon, and it will handle all of the removal and clean up of all of the Oxide files for you. If you switch to Vanilla from either Carbon or Oxide, it will make sure those files are cleaned up as well.

You also have the ability to set a "Modding Root" folder. This folder is very important, as it allows you to have different plugins, configs, and data for different wipes or maps. Say you are running a proc gen map, and you are running a set of plugins that makes sense to have on a proc gen map, then you decide on wipe day to switch to a spooky, Halloween themed map. Obviously you'll probably want to have some different plugins running on that custom Halloween themed map. You can make that switch easily by just specifying the "Modding Root" folder that you want to use, instead of having to delete files, configs, etc.

## Pterodactyl Disclaimer

This guide assumes that you have already installed Pterodactyl panel, and are familiar with how to set up servers. You should also already have a location, a node, and ports already allocated on that node. If you don't know how to do any of this, or you missed a step, please refer to the Pterodactyl Panel installation instructions below. A link to their Discord server is also below for you to get support during installation. They however **do not** support Carbon specific questions, only questions relating to Pterodactyl panel itself. Just keep that in mind.

[Pterodactyl Installation Instructions](https://pterodactyl.io/panel/1.0/getting_started.html)

[Pterodactyl Discord](https://discord.gg/pterodactyl)

## Difference Between Carbon Builds

The difference between the Production, Preview, and Edge builds of Carbon are:

**Production** - The most stable version of Carbon. Updated once every few weeks.

**Preview** - Updated frequently, contains future features for testing, and you will run into a few bugs here and there.

**Edge** - Like living on the edge? This is the most current version of Carbon, and it used mainly by developers and server owners to test brand new features of Carbon that are still in the Beta development stage. Expect some bugs.

One other thing is the difference between the Minimal and Standard versions of Carbon. The minimal version of Carbon does **not** contain the Admin Module, CarbonAuto, or the Zip Dev Script Processor. Its basically a lightweight version of carbon, stripping away the QoL features and focuses only on plugin execution. Its not like minimal is *faster* then the Standard build, it just has less "clutter".

## Adding The Egg To The Nest

First we need to add the egg to the Rust nest. Here are the steps.

1. Login to the admin dashboard of your Pterodactyl panel installation.

2. Click on the "Nests" link in the side bar on the left.

3. Since there is already a "Rust" nest, we don't have to create a new one. Lets just go ahead and add the egg to the nest. Click on the green "Import Egg" button on the right.

4. Select the Custom Carbon Egg that you just downloaded by clicking browse, then navigate to the location you saved the egg to, and double click the file.

5. Next we need to select the "Rust" nest under the "Associated Nest" field.

   ![Import Egg Image](https://raw.githubusercontent.com/SturdyStubs/AIO.Egg/main/images/import_egg_all_carbon.png)

6. Now all we have to do is click on "Import".

### Installing the Server

This server installation guide is very similar to the Custom Rust Egg by MikeHawk, with some key differences. Some of the steps for installation might be the same. Please make sure to read these installation instructions throughly.

1. Log into your admin dashboard of your panel.

2. Navigate to your Servers by clicking on "Servers" on the side bar.

3. Click the "Create New" button on the right

4. Configure your server details in the "Core Details" section

5. For your port allocations you are going to need 1 main port, and 3 additional allocations. These allocations are for the Query Port, RCON Port, and App Port.

   ![Allocation Management Image](https://raw.githubusercontent.com/SturdyStubs/AIO.Egg/main/images/allocation_management.png)

6. Configure your "Application Feature Limits" and "Resource Management" sections to your liking

7. Under "Nest Configuration", select the "Rust" Nest

8. Then if your "Egg" field does not already say "Rust Carbon", change it to "Rust Carbon".

   ![Nest Configuration Image](https://raw.githubusercontent.com/SturdyStubs/AIO.Egg/main/images/nest_configuration_all_carbon.png)

9. The "Docker Configuration" section can be skipped.

10. Next is the big part. The "Startup Configuration" section. In this section, you can fill out everything pretty much to your liking. However there are a few new options here that are not apart of the Default Rust Egg.

    1. Under the "Modding Framework" variable, you can choose different options for either Carbon, Oxide, or Vanilla. This is a combined version of the "Carbon Build" and "Minimal" variables from the other Custom Rust Egg by MikeHawk. The key difference here is this egg is also set up for the staging branch of Rust as well. The Staging Branch is only available with Carbon. See the "Difference Between Carbon Builds" section at the top of this page for more information.
    2. Lastly, the major difference between the Default Rust egg, and the Carbon Rust egg, is that you can set an IP address for your Rust+ App. This is critical in ensuring that your Rust+ connection is able to connect to the Rust+ API. Set this value to the public IP address of your server.
    3. Additionally, you can configure different Carbon/Oxide root directories. This is good if you want to run a certain set of plugins on one map, but don't want to go through the hassle of copying and pasting over different configs for that map. All you have to do is just change your Carbon directory, and it will automatically switch over to those plugins, configs, and data files.
       1. An important thing to note is that the "Modding Root" variable should be set appropriately. If you're running a build of Carbon, your "Modding Root" should have the word "carbon" in it. Same thing for Oxide. If you're running Oxide, your "Modding Root" variable should have the word "oxide" in it. The vanilla option does not need to have the variable set.

11. Do not forget to set your RCON, Query, and App ports to the appropriate ports that you assigned under the "Core Details" section. These ports should be equal to one of the three ports you assigned under your "Additional Ports" section.

12. Start your server by clicking the green "Create Server" button at the bottom of the page.

And that's it! You now have a Custom Carbon Rust server installed and ready to use!
