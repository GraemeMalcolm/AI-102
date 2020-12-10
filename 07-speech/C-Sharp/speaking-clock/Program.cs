﻿using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;

// Import namespaces


namespace speaking_clock
{
    class Program
    {
        private static SpeechConfig speechConfig;
        static async Task Main(string[] args)
        {
            try
            {
                // Get config settings from AppSettings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string cogSvcKey = configuration["CognitiveServiceKey"];
                string cogSvcRegion = configuration["CognitiveServiceRegion"];

                // Configure speech service


                Console.WriteLine("Say 'stop' to end");
                string command = "";
                while (command.ToLower() != "stop.")
                {
                    command = await TranscribeCommand();
                    if (command.ToLower()=="what time is it?")
                    {
                        await TellTime();
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static async Task<string> TranscribeCommand()
        {
            string command = "stop.";
            
            // Configure speech recognition


            // Process speech input


            // Return the command
            return command;
        }

        static async Task TellTime()
        {
            var now = DateTime.Now;
            string responseText = "The time is " + now.Hour.ToString() + ":" + now.Minute.ToString("D2");
                        
            // Configure speech synthesis


            // Synthesize spoken output


            // Print the response
            Console.WriteLine(responseText);
        }

    }
}
