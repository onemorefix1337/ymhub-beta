using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.IO;

class Program {
    static void Main(string[] args) {
        if (args.Length < 2) return;
        string wsUrl = args[0].Replace("localhost", "127.0.0.1");
        string jsonPayload = args[1];
        try {
            using (var ws = new ClientWebSocket()) {
                ws.Options.KeepAliveInterval = TimeSpan.Zero;
                ws.ConnectAsync(new Uri(wsUrl), CancellationToken.None).Wait();
                var bytes = Encoding.UTF8.GetBytes(jsonPayload);
                ws.SendAsync(new ArraySegment<byte>(bytes), WebSocketMessageType.Text, true, CancellationToken.None).Wait();
                
                var buffer = new byte[1024 * 1024];
                var result = ws.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None).Result;
                string res = Encoding.UTF8.GetString(buffer, 0, result.Count);
                Console.WriteLine(res);
            }
        } catch (Exception ex) {
            Console.WriteLine("Error: " + ex.Message);
        }
    }
}
