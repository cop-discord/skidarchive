const Discord = require("discord.js-selfbot-v11"); 
const { token } = require("./config.json");
const chalk = require("chalk"); 
const keepAlive = require("./server");
const client = new Discord.Client({
  ws: { properties: { $browser: "Discord iOS" } },
});

client.on("ready", () => {
  console.clear();
  console.log(chalk.magentaBright`Mobile Status Applied to ${client.user.tag}`);
});
keepAlive();
client.login(token);

//Instructions:
//Make a env in secrets named "TOKEN" and put your token in value and run it and host it 24/7 with https://uptimerobot.com
