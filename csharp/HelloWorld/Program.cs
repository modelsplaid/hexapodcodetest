// See https://aka.ms/new-console-template for more information

using System;

    static void Main()
    {
        // Get the current system timestamp
        DateTime now = DateTime.Now;

 
        // Convert to Unix timestamp (float)
        float unixTimestamp = (float)(now.Subtract(new DateTime(1970, 1, 1))).TotalMilliseconds;
        Console.WriteLine("Unix Timestamp (float): " + unixTimestamp.ToString());

        // Convert to formatted string "year.month.day"
        string formattedDate = now.ToString("yyyy.MM.dd");
        Console.WriteLine("Formatted Date: " + formattedDate);

        // If you need more detailed formatting like "year.month.day.hour.minute.second"
        string detailedFormattedDate = now.ToString("yyyy.MM.dd.HH.mm.ss");
        Console.WriteLine("Detailed Formatted Date: " + detailedFormattedDate);
    }




DateTime now = DateTime.UtcNow;
long unixTimestampMs = ((DateTimeOffset)now).ToUnixTimeMilliseconds();
Console.WriteLine(unixTimestampMs.ToString("D12")); // "D12" ensures a 12-digit number with padding if necessary


//Main();
// static void test_time_stamp(){
//     DateTime now = DateTime.Now;
//     float unixTimestamp = (float)(now.Subtract(new DateTime(1970, 1, 1))).TotalSeconds;
//     Console.WriteLine("Unix Timestamp (float): " + unixTimestamp);
// }

//test_time_stamp();


