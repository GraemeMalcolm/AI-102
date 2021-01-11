using System;
using System.IO;
using System.Drawing;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json.Linq;

// Import namespaces
using Microsoft.Azure.CognitiveServices.Vision.ComputerVision;
using Microsoft.Azure.CognitiveServices.Vision.ComputerVision.Models;

namespace image_analysis
{
    class Program
    {

        private static ComputerVisionClient cvClient;
        static async Task Main(string[] args)
        {
            try
            {
                // Get config settings from AppSettings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string cogSvcEndpoint = configuration["CognitiveServicesEndpoint"];
                string cogSvcKey = configuration["CognitiveServiceKey"];

                // Authenticate Computer Vision client
                ApiKeyServiceClientCredentials credentials = new ApiKeyServiceClientCredentials(cogSvcKey);
                cvClient = new ComputerVisionClient(credentials)
                {
                    Endpoint = cogSvcEndpoint
                };

                // Get image
                string imageFile = "images/building.jpg";

                // Get captions
                await GetImageCaption(imageFile);

                // Get landmarks
                await GetLandmarks(imageFile);
               
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static async Task GetImageCaption(string imageFile)
        {
            using (var imageData = File.OpenRead(imageFile))
            {
               var results = await cvClient.DescribeImageInStreamAsync(imageData);
               foreach (var caption in results.Captions)
                {
                    Console.WriteLine($"Description: {caption.Text} (confidence: {caption.Confidence.ToString("P")})");
                }
            }
        }

        static async Task GetLandmarks(string imageFile)
        {
            using (var imageData = File.OpenRead(imageFile))
            {
                DomainModelResults response = await cvClient.AnalyzeImageByDomainInStreamAsync("Landmarks", imageData);
                Console.WriteLine("Landmarks:");
                foreach (var landmark in JObject.Parse(response.Result.ToString())["landmarks"])
                {
                    Console.WriteLine($" - {landmark["name"]} (confidence: {landmark["confidence"]})");
                }

            }
        }

    }
}
