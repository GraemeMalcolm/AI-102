using System;
using System.IO;
using System.Linq;
using System.Drawing;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;

// Import namespaces
using Microsoft.Azure.CognitiveServices.Vision.Face;
using Microsoft.Azure.CognitiveServices.Vision.Face.Models;

namespace analyze_faces
{
    class Program
    {

        private static FaceClient faceClient;
        static async Task Main(string[] args)
        {
            try
            {
                // Get config settings from AppSettings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string cogSvcEndpoint = configuration["CognitiveServicesEndpoint"];
                string cogSvcKey = configuration["CognitiveServiceKey"];

                // Authenticate Face client
                ApiKeyServiceClientCredentials credentials = new ApiKeyServiceClientCredentials(cogSvcKey);
                faceClient = new FaceClient(credentials)
                {
                    Endpoint = cogSvcEndpoint
                };

                Console.WriteLine("1: Detect faces\n2: Compare faces\n3: Train a facial recognition model\n4: Recognize faces\n5: Verify a face\nAny other key to quit");
                Console.WriteLine("Enter a number:");
                string command = Console.ReadLine();
                switch (command)
                {
                    case "1":
                        await DetectFaces("images/people.jpg");
                        break;
                    case "2":
                        string personImage = "images/person1.jpg"; // Also try person2.jpg
                        await CompareFaces(personImage, "images/people.jpg");
                        break;
                    case "3":
                        List<string> folders = new List<string>(){"Mary", "Sue"};
                        await TrainModel("employees_group", "employees", folders);
                        break;
                    case "4":
                        await RecognizeFaces("images/people2.jpg", "employees_group");
                        break;
                    case "5":
                        await VerifyFace("images/person1.jpg", "Mary", "employees_group");
                        break;
                    default:
                        break;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static async Task DetectFaces(string imageFile)
        {
            Console.WriteLine($"Detecting faces in {imageFile}");

            // Specify facial features to be retrieved
            List<FaceAttributeType?> features = new List<FaceAttributeType?>
            {
                FaceAttributeType.Age,
                FaceAttributeType.Emotion,
                FaceAttributeType.Glasses
            };

            // Get image analysis
            using (var imageData = File.OpenRead(imageFile))
            {    
                var faces = await faceClient.Face.DetectWithStreamAsync(imageData, returnFaceAttributes: features);

                    // Get faces
                    if (faces.Count > 0)
                    {
                        Console.WriteLine($"{faces.Count} faces detected.");

                        // Prepare image for drawing
                        Image image = Image.FromFile(imageFile);
                        Graphics graphics = Graphics.FromImage(image);
                        Pen pen = new Pen(Color.LightGreen, 3);
                        Font font = new Font("Arial", 4);
                        SolidBrush brush = new SolidBrush(Color.White);

                        // Draw and annotate each face
                        foreach (var face in faces)
                        {
                            // Get face properties
                            Console.WriteLine($"\nFace ID: {face.FaceId}");
                            Console.WriteLine($" - Age: {face.FaceAttributes.Age}");
                            Console.WriteLine($" - Emotions:");
                            foreach (var emotion in face.FaceAttributes.Emotion.ToRankedList())
                            {
                                Console.WriteLine($"   - {emotion}");
                            }

                            Console.WriteLine($" - Glasses: {face.FaceAttributes.Glasses}");

                            // Draw and annotate face
                            var r = face.FaceRectangle;
                            Rectangle rect = new Rectangle(r.Left, r.Top, r.Width, r.Height);
                            graphics.DrawRectangle(pen, rect);
                            string annotation = $"Face ID: {face.FaceId}";
                            graphics.DrawString(annotation,font,brush,r.Left, r.Top);
                        }

                        // Save annotated image
                        String output_file = "detected_faces.jpg";
                        image.Save(output_file);
                        Console.WriteLine(" Results saved in " + output_file);   
                    }
            }
                
        
        }

        static async Task CompareFaces(string image1, string image2)
        {
            Console.WriteLine($"Comparing faces in {image1} and {image2}");
        
        }

        static async Task TrainModel(string groupId, string groupName, List<string> imageFolders)
        {
            Console.WriteLine($"Creating model for {groupId}");
        
        }

        static async Task RecognizeFaces(string imageFile, string groupId)
        {
            Console.WriteLine($"Recognizing faces in {imageFile}");
        
        }

        static async Task VerifyFace(string personImage, string personName, string groupId)
        {
            Console.WriteLine($"Verifying the person in {personImage} is {personName}");
        
        }


    }
}
