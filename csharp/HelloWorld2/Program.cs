// See https://aka.ms/new-console-template for more information
//Console.WriteLine("Hello, World!");

using System;
using System.Runtime.InteropServices;
namespace HelloWorld
{
  class Program
  {
    static void Main(string[] args)
    {
        int a = 3;
        int size = Marshal.SizeOf(typeof(int));
        Console.WriteLine(size);

        Console.Write("tzq"); 
        Console.WriteLine("Hello World123!");    
    }
  }
}

/*
3D FloTrix® megaSPIN软硬件系统
一．硬件系统：

硬件系统框图如下。用户图形化交互设备和控制主机采用两台独立设备。这样做有以下三个目的：
1.可以提高系统的稳定性：当用户界面出问题时工控机仍然可以正常运行。
2.控制逻辑和交互代码完全独立：升级或修改其中一部分代码时，另一部分不会受到		影响。方便升级。
3.可扩展性更强：可根据应用需求适配不同规格的工控机和平板显示屏。

平板显示屏和工控机之间采用TCP通信，这样可以保证程序的跨平台通信时的兼容性。另外，在项目初期，平板显示屏内的程序仍可以运行在工控机内，方便较快速的出效果。

二．软件系统：

软件系统分为两部分，一部分为运行在工控机上的控制程序，另一部分为运行在平板上的用户交互程序。


控制程序：

控制程序完成的功能有：
1.接收来自用户的控制信号并转发到硬件（如电机启停，阀门开关等）。
2.接收来自硬件传感器（如电机转速，气泡检测传感器，温度传感器）的数据。
3.传感器数据实时记录并存储本地。
4.同时发送给GUI交互程序，显示当前数据。

控制程序整体流程图如下：

程序稳定性测试方案：
1.CPU占用率异常测试：
(1)是否有线程/进程持续占满一个核？
(2)是否仅仅启动一两个核，其他CPU核没有得到有效利用？

2.内存占用异常测试：
(1)是否有线程/进程使用的内存在随时间的增加而增加？
(2)是否内存长期处于较高状态（大于80%）？

3.传感器数据读取问题：
(1)是否数据传输延时过大？
(2)缓存占满后数据保留方式：保留最新的数据？或 先入先出？

GUI交互程序：


三．风险点：

尽管C#语言加AvaloniaUI的方式可以跨平台运行，可支持Linux及Windows等系统。从目前的BUG问题反馈来看，基于Linux系统的AvaloniaUI的问题要比Windows的多一些。如下两图。
数据来源：
https://github.com/AvaloniaUI/Avalonia/issues?q=is%3Aissue+is%3Aopen+linux+label%3Aos-linux
https://github.com/AvaloniaUI/Avalonia/issues?q=is%3Aissue+is%3Aopen+linux+label%3Aos-windows

建议1：
虽然AvaloniaUI+C#的方案可能有一定的潜在风险，但是结合目前的团队情况以及产品	进度要求，目前可以先采用这套方案进行。另外，即使AvaloniaUI的稳定性出现问题，	因为目前的方案是控制程序（c++）和 GUI交互程序（C#）分开的设计，理论上用	户交互的问题不会传导到设备关键部件的运行。

建议2：
提前进行一些系统兼容性测试工作，摸清潜在的问题点/BUGS，评估是否对项目会造	成较大影响。

比如：
1.是否某个AvaloniaUI和Linux版本的搭配会存在问题。如果有，是否有替代的		版本？
2.某些组件是否存在限制，是否有替代方案？
3.在GUI程序运行在工控机上，工控机连接触摸屏的方案下。触摸屏的驱动是否		能适配？最好买一套触摸屏进行测试。           

建议3：
本来我考虑的是用PLC来做数据到工控机之间的转发。但是和团队交流后发现，后面	准备采用串口服务器做转发。如果我们之前没有在设备中用过串口服务器，是否需要提	前做一下串口服务器的稳定性测试？


*/