API 文档：https://api.flutter.dev/flutter

[本章目录 | 《Flutter 实战·第二版》 (flutterchina.club)](https://book.flutterchina.club/chapter1/)

> flutter json 转 model，使用 json_to_model

**flutter 构建 apk**

```cmd
flutter build apk
```

> 如果发现构建的 apk 在 debug 模式下能用，但是在 release 模式下不能用，如果 app 中使用了动态链接库，那么很有可能是因为 release 模式的 apk 没有加上动态链接库，需要检查一下。

如果有多个入口文件，可以用如下方式编译 apk

```cmd
flutter build apk -t lib\main_1.dart
```

## Java/Kotlin 插件开发


> [!WARNING] Title
> 如果需要在 flutter 端和原生端之间传输大量数据，两者之间的通信是需要花费明显的时间，可能达到 20ms。

### 基本知识

#### 如何创建插件

在开发 flutter 应用时，有时需要自己开发原生插件，创建插件的命令如下

```sh
flutter create --org com.example -t plugin --platform android plugin_name
```

默认使用 kotlin 语言创建项目，如果需要指定 java 语言，需要在后面加上 `-a java`

```sh
flutter create --org com.example -t plugin --platform android plugin_name -a java
```

如果想在已经创建好的工程添加新的平台

```sh
flutter create --template=plugin --platforms=web .
```


创建好的插件工程具体有以下三个目录

- android: Android 的原生代码
- example: 一个 Flutter 的实例项目，用来展示、测试你开发的 plugin 的
- lib: Plugin 的 Dart 代码

假设创建了一个插件工程 `test_plugin`，最好不要通过 android studio 打开 `test_plugin` 来修改原生代码，而是要打开 `test_plugin/android` 来修改原生代码，这样才能正确地构建项目，同步 gradle 包。此外还需要在 `android\build.gradle` 中添加下面这些内容配置 flutter

```gradle
//获取local.properties配置文件  
def localProperties = new Properties()  
def localPropertiesFile = rootProject.file('local.properties')  
if (localPropertiesFile.exists()) {  
    localPropertiesFile.withReader('UTF-8') { reader ->  
        localProperties.load(reader)  
    }  
}  
//获取flutter的sdk路径  
def flutterRoot = localProperties.getProperty('flutter.sdk')  
if (flutterRoot == null) {  
    throw new GradleException("Flutter SDK not found. Define location with flutter.sdk in the local.properties file.")  
}  
  
dependencies {  
    implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk7:$kotlin_version"  
    compileOnly files("$flutterRoot/bin/cache/artifacts/engine/android-arm/flutter.jar")  
    compileOnly 'androidx.annotation:annotation:1.1.0'  
    implementation 'androidx.core:core:1.6.0'
}
```


#### 本地使用插件

在 flutter 工程目录中新建 plugins 文件夹用来存放本地插件，在 `pubspec.yaml` 中添加以下代码

```yaml
dependencies:
  flutter:
    sdk: flutter

  # The following adds the Cupertino Icons font to your application.
  # Use with the CupertinoIcons class for iOS style icons.
  cupertino_icons: ^0.1.2
#pub插件引用
#  webview_flutter: ^0.3.0

#本地插件引用 注意缩进格式
  webview_flutter:
    path: plugins/webview_flutter
```


如果插件中申请了额外的权限和服务，也需要在 android/src/main/AndroidManifest.xml 注明，直接从插件声明的地方复制粘贴过来即可。


#### 上传插件

[Flutter | 如何优雅的开发一个插件并发布到 Dart 仓库？如何开发 Flutter 插件，并发布到 Dart 仓库 - 掘金](https://juejin.cn/post/6961565875035963399)

注意修改 pubspec.yaml 中的 descrpition、添加 repository，此外还需要修改 License。


### 录制系统播放的声音

该插件基于 flutter 包 [flutter_screen_recording](https://pub.dev/packages/flutter_screen_recording) 和 github 库 [SystemAudioCaptureAndroid](https://github.com/HarshSinghRajawat/SystemAudioCaptureAndroid)，实现了在安卓手机上录制系统播放声音的功能，也就是说，只要一个安卓应用没有 [设置不允许其它应用录制声音](https://developer.android.google.cn/media/platform/av-capture?hl=en#constraining_capture_by_other_apps)，该插件可以录制该应用播放的声音。

Github 地址：[Xiang-M-J/flutterSystemAudioRecorder](https://github.com/Xiang-M-J/flutterSystemAudioRecorder)


#### 创建工程


创建插件工程

```sh
flutter create -t plugin --platform android system_audio_recorder
```

创建好的插件工程主要关注的是以下三个目录

- android：Android 的原生代码
- example：一个 Flutter 的实例项目，用来展示、测试开发的 plugin
- lib：Plugin 的 Dart 代码


#### 原生代码

用 android studio 打开 `system_audio_recorder/android`，开始修改配置。打开 `system_audio_recorder/android/gradle/wrapper/gradle-warpper.properties`，将 distributionUrl 修改为 `file:///D://work//app//gradle-7.5-all.zip`。打开 `system_audio_recorder/android/build.gradle` 在文件末尾添加配置 flutter 和 androidx.core 的代码

```
//获取local.properties配置文件  
def localProperties = new Properties()  
def localPropertiesFile = rootProject.file('local.properties')  
if (localPropertiesFile.exists()) {  
    localPropertiesFile.withReader('UTF-8') { reader ->  
        localProperties.load(reader)  
    }  
}  
//获取flutter的sdk路径  
def flutterRoot = localProperties.getProperty('flutter.sdk')  
if (flutterRoot == null) {  
    throw new GradleException("Flutter SDK not found. Define location with flutter.sdk in the local.properties file.")  
}  
  
dependencies {  
    implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk7:$kotlin_version"  
    compileOnly files("$flutterRoot/bin/cache/artifacts/engine/android-arm/flutter.jar")  
    compileOnly 'androidx.annotation:annotation:1.1.0'  
    implementation 'androidx.core:core:1.6.0'
}
```

点击 sync Now，同步 gradle 包。

`kotlin/com/example/system_audio_recorder/` 已经有 `SystemAudioRecorderPlugin.kt` ，这个文件用来实现插件的各种方法，但是由于需要录音系统声音，需要使用前台服务，所以需要额外添加一个 `ForegroundService.kt` 文件用于配置前台服务，`ForegroundService.kt` 的内容如下：


> [!WARNING] 
> ForegroundService 的 package 不能和 SystemAudioRecorderPlugin 的 package 一致，否则在启动服务时会报错！！！


```kotlin
package com.foregroundservice  

import android.Manifest  
import android.app.Activity  
import android.app.NotificationChannel  
import android.app.NotificationManager  
import android.app.PendingIntent  
import android.app.Service  
import android.content.Context  
import android.content.Intent  
import android.content.pm.PackageManager  
import android.os.Build  
import android.os.IBinder  
import android.util.Log  
import androidx.core.app.ActivityCompat  
import androidx.core.app.NotificationCompat  
import androidx.core.content.ContextCompat  
import com.example.system_audio_recorder.SystemAudioRecorderPlugin  
  
class ForegroundService : Service() {  
    private val CHANNEL_ID = "ForegroundService Kotlin"  
    private val REQUEST_CODE_MEDIA_PROJECTION = 1001  
    // 静态方法，SystemAudioRecorderPlugin 会调用这些方法  
    companion object {  
        fun startService(context: Context, title: String, message: String) {  
            println("-------------------------- startService");  
            try {  
                val startIntent = Intent(context, ForegroundService::class.java)  
                startIntent.putExtra("messageExtra", message)  
                startIntent.putExtra("titleExtra", title)  
                println("-------------------------- startService2");  
  
                ContextCompat.startForegroundService(context, startIntent)  
                println("-------------------------- startService3");  
  
            } catch (err: Exception) {  
                println("startService err");  
                println(err);  
            }  
        }  
  
        fun stopService(context: Context) {  
            val stopIntent = Intent(context, ForegroundService::class.java)  
            context.stopService(stopIntent)  
        }  
    }  
    // 在 SystemAudioRecorderPlugin 调用 ActivityCompat.startActivityForResult 时调用  
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {  
        try {  
            Log.i("ForegroundService", "onStartCommand")  
            // Verification permission en Android 14 (SDK 34)  
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {  
                if (ContextCompat.checkSelfPermission(this, Manifest.permission.FOREGROUND_SERVICE_MEDIA_PROJECTION)  
                    != PackageManager.PERMISSION_GRANTED) {  
                    Log.i("Foreground","MediaProjection permission not granted, requesting permission")  
  
                    ActivityCompat.requestPermissions(  
                        this as Activity,  
                        arrayOf(Manifest.permission.FOREGROUND_SERVICE_MEDIA_PROJECTION),  
                        REQUEST_CODE_MEDIA_PROJECTION  
                    )  
                } else {  
                    startForegroundServiceWithNotification(intent)  
                }  
            } else {  
                startForegroundServiceWithNotification(intent)  
            }  
  
            return START_NOT_STICKY  
        } catch (err: Exception) {  
            Log.e("ForegroundService", "onStartCommand error: $err")  
        }  
        return START_STICKY  
    }  
    private fun startForegroundServiceWithNotification(intent: Intent?) {  
  
        createNotificationChannel()  
        val notificationIntent = Intent(this, SystemAudioRecorderPlugin::class.java)  
  
        val pendingIntent = PendingIntent.getActivity(  
            this, 0, notificationIntent, PendingIntent.FLAG_MUTABLE  
        )  
  
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)  
            .setContentIntent(pendingIntent)  
            .build()  
  
        startForeground(1, notification)  
        Log.i("ForegroundService", "startForegroundServiceWithNotification")  
    }  
  
    override fun onBind(intent: Intent): IBinder? {  
        return null  
    }  
  
    private fun createNotificationChannel() {  
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {  
            val serviceChannel = NotificationChannel(  
                CHANNEL_ID, "Foreground Service Channel", NotificationManager.IMPORTANCE_DEFAULT  
            )  
            val manager = getSystemService(NotificationManager::class.java)  
            manager!!.createNotificationChannel(serviceChannel)  
        }  
    }  
  
}
```


`SystemAudioRecorderPlugin` 的内容如下

```kotlin
package com.example.system_audio_recorder  
  
import android.annotation.SuppressLint  
import android.app.Activity  
import android.content.Context  
import android.content.Intent  
import android.media.AudioAttributes  
import android.media.AudioFormat  
import android.media.AudioPlaybackCaptureConfiguration  
import android.media.AudioRecord  
import android.media.projection.MediaProjection  
import android.media.projection.MediaProjectionManager  
import android.os.Build  
import android.os.Environment  
import android.util.Log  
import androidx.annotation.RequiresApi  
import androidx.core.app.ActivityCompat  
  
import io.flutter.embedding.engine.plugins.FlutterPlugin  
import io.flutter.embedding.engine.plugins.activity.ActivityAware  
import io.flutter.embedding.engine.plugins.activity.ActivityPluginBinding  
import io.flutter.plugin.common.MethodCall  
import io.flutter.plugin.common.MethodChannel  
import io.flutter.plugin.common.MethodChannel.MethodCallHandler  
import io.flutter.plugin.common.MethodChannel.Result  
import io.flutter.plugin.common.PluginRegistry  
import java.io.DataInputStream  
import java.io.DataOutputStream  
import java.io.File  
import java.io.FileInputStream  
import java.io.FileNotFoundException  
import java.io.FileOutputStream  
import java.io.IOException  
import java.nio.ByteBuffer  
import java.nio.ByteOrder  
import java.text.SimpleDateFormat  
import java.util.Date  
import com.foregroundservice.ForegroundService  
  
/** SystemAudioRecorderPlugin */  
class SystemAudioRecorderPlugin: MethodCallHandler, PluginRegistry.ActivityResultListener, FlutterPlugin,  
  ActivityAware {  
  
  private lateinit var channel : MethodChannel  
  private var mProjectionManager: MediaProjectionManager? = null  
  private var mMediaProjection: MediaProjection? = null  
  private var mFileName: String? = ""  
  private val RECORD_REQUEST_CODE = 333  
  var TAG: String = "system_audio_recorder"  
  
  private lateinit var _result: Result  
  
  private var pluginBinding: FlutterPlugin.FlutterPluginBinding? = null  
  private var activityBinding: ActivityPluginBinding? = null;  
  var recordingThread: Thread? = null  
  private val bufferElements2Record = 1024  
  private val bytesPerElement = 2  
  private var mAudioRecord: AudioRecord? = null  
  private var isRecording: Boolean = false  
  private var RECORDER_SAMPLERATE: Int = 44100  
  val RECORDER_CHANNELS: Int = AudioFormat.CHANNEL_IN_MONO  
  val RECORDER_AUDIO_ENCODING: Int = AudioFormat.ENCODING_PCM_16BIT  
  private var root: File? = null  
  private var cache: File? = null  
  private var rawOutput: File? = null  
  
  override fun onAttachedToEngine(flutterPluginBinding: FlutterPlugin.FlutterPluginBinding) {  
    pluginBinding = flutterPluginBinding;  
  }  
  
  @RequiresApi(Build.VERSION_CODES.Q)  
  // 在 ForegroundService 的startCommand执行完后执行  
  override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?): Boolean {  
    if (requestCode == RECORD_REQUEST_CODE) {  
      if (resultCode == Activity.RESULT_OK) {  
        mMediaProjection = mProjectionManager?.getMediaProjection(resultCode, data!!)  
        startRecording(mMediaProjection!!)  
        _result.success(true)  
        return true  
      } else {  
        _result.success(false)  
      }  
    }  
    return false  
  }  
  
  override fun onMethodCall(call: MethodCall, result: Result) {  
    val appContext = pluginBinding!!.applicationContext  
  
    if (call.method == "getPlatformVersion") {  
      result.success("Android ${Build.VERSION.RELEASE}")  
    } else if (call.method == "startRecord"){  
      try {  
        _result = result  
        val sampleRate = call.argument<Int?>("sampleRate")  
        if (sampleRate != null){  
          RECORDER_SAMPLERATE = sampleRate  
        }  
  
        ForegroundService.startService(appContext, "开始录音", "开始录音")  
        mProjectionManager =  
          appContext.getSystemService(  
            Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager?  
  
        val permissionIntent = mProjectionManager?.createScreenCaptureIntent()  
        Log.i(TAG, "startActivityForResult")  
        // 调用 ForegroundService的 startCommand 方法  
        ActivityCompat.startActivityForResult(  
          activityBinding!!.activity,  
          permissionIntent!!,  
          RECORD_REQUEST_CODE,  
          null  
        )  
      } catch (e: Exception) {  
        Log.e(TAG, "Error onMethodCall startRecord: ${e.message}")  
        result.success(false)  
      }  
    }  
    else if (call.method == "stopRecord"){  
      Log.i(TAG, "stopRecord")  
      try {  
        ForegroundService.stopService(appContext)  
        if (mAudioRecord != null){  
          stop()  
          result.success(mFileName)  
        }else{  
          result.success("")  
        }  
      } catch (e: Exception) {  
        result.success("")  
      }  
    }  
    else {  
      result.notImplemented()  
    }  
  }  
  
  @RequiresApi(api = Build.VERSION_CODES.Q)  
  fun startRecording(mProjection: MediaProjection): Boolean {  
    Log.i(TAG, "startRecording")  
    if (mAudioRecord == null){  
      val config : AudioPlaybackCaptureConfiguration  
      try {  
        config = AudioPlaybackCaptureConfiguration.Builder(mProjection)  
          .addMatchingUsage(AudioAttributes.USAGE_MEDIA)  
          .addMatchingUsage(AudioAttributes.USAGE_GAME)  
          .build()  
      } catch (e: NoClassDefFoundError) {  
        return false  
      }  
      val format = AudioFormat.Builder()  
        .setEncoding(RECORDER_AUDIO_ENCODING)  
        .setSampleRate(RECORDER_SAMPLERATE)  
        .setChannelMask(RECORDER_CHANNELS)  
        .build()  
  
      mAudioRecord = AudioRecord.Builder().setAudioFormat(format).setBufferSizeInBytes(bufferElements2Record).setAudioPlaybackCaptureConfig(config).build()  
      isRecording = true  
      mAudioRecord!!.startRecording()  
  
      createAudioFile()  
  
      recordingThread = Thread({ writeAudioFile() }, "System Audio Capture")  
  
      recordingThread!!.start()  
  
    }  
    return true  
  }  
  
  @Throws(IOException::class)  
  private fun rawToWave(rawFile: File, waveFile: File) {  
    val rawData = ByteArray(rawFile.length().toInt())  
    var input: DataInputStream? = null  
    try {  
      input = DataInputStream(FileInputStream(rawFile))  
      input.read(rawData)  
    } finally {  
      input?.close()  
    }  
  
    var output: DataOutputStream? = null  
    try {  
      output = DataOutputStream(FileOutputStream(waveFile))  
  
      // WAVE header  
      writeString(output, "RIFF") // chunk id  
      writeInt(output, 36 + rawData.size) // chunk size  
      writeString(output, "WAVE") // format  
      writeString(output, "fmt ") // subchunk 1 id  
      writeInt(output, 16) // subchunk 1 size  
      writeShort(output, 1.toShort()) // audio format (1 = PCM)  
      writeShort(output, 1.toShort()) // number of channels  
      writeInt(output, RECORDER_SAMPLERATE) // sample rate  
      writeInt(output, RECORDER_SAMPLERATE) // byte rate  
      writeShort(output, 2.toShort()) // block align  
      writeShort(output, 16.toShort()) // bits per sample  
      writeString(output, "data") // subchunk 2 id  
      writeInt(output, rawData.size) // subchunk 2 size  
      // Audio data (conversion big endian -> little endian)      
      val shorts = ShortArray(rawData.size / 2)  
      ByteBuffer.wrap(rawData).order(ByteOrder.LITTLE_ENDIAN).asShortBuffer()[shorts]  
      val bytes = ByteBuffer.allocate(shorts.size * 2)  
      for (s in shorts) {  
        bytes.putShort(s)  
      }  
  
      output.write(fullyReadFileToBytes(rawFile))  
    } finally {  
      output?.close()  
    }  
  }  
  
  @Throws(IOException::class)  
  fun fullyReadFileToBytes(f: File): ByteArray {  
    val size = f.length().toInt()  
    val bytes = ByteArray(size)  
    val tmpBuff = ByteArray(size)  
    val fis = FileInputStream(f)  
    try {  
      var read = fis.read(bytes, 0, size)  
      if (read < size) {  
        var remain = size - read  
        while (remain > 0) {  
          read = fis.read(tmpBuff, 0, remain)  
          System.arraycopy(tmpBuff, 0, bytes, size - remain, read)  
          remain -= read  
        }  
      }  
    } catch (e: IOException) {  
      throw e  
    } finally {  
      fis.close()  
    }  
  
    return bytes  
  }  
  
  private fun createAudioFile() {  
  
    root = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MUSIC), "/Audio Capture")  
//    val mFilename: String? = pluginBinding!!.applicationContext.externalCacheDir?.absolutePath  
//    root = File(mFilename)  
    cache = File(pluginBinding!!.applicationContext.cacheDir.absolutePath, "/RawData")  
    if (!root!!.exists()) {  
      root!!.mkdir()  
      root!!.setWritable(true)  
    }  
    if (!cache!!.exists()) {  
      cache!!.mkdir()  
      cache!!.setWritable(true)  
      cache!!.setReadable(true)  
    }  
  
    rawOutput = File(cache, "raw.pcm")  
  
    try {  
      rawOutput!!.createNewFile()  
    } catch (e: IOException) {  
      Log.e(TAG, "createAudioFile: $e")  
      e.printStackTrace()  
    }  
  
    Log.d(TAG, "path: " + rawOutput!!.absolutePath)  
  
  }  
  
  @Throws(IOException::class)  
  private fun writeInt(output: DataOutputStream, value: Int) {  
    output.write(value shr 0)  
    output.write(value shr 8)  
    output.write(value shr 16)  
    output.write(value shr 24)  
  }  
  
  @Throws(IOException::class)  
  private fun writeShort(output: DataOutputStream, value: Short) {  
    output.write(value.toInt() shr 0)  
    output.write(value.toInt() shr 8)  
  }  
  
  @Throws(IOException::class)  
  private fun writeString(output: DataOutputStream, value: String) {  
    for (element in value) {  
      output.write(element.code)  
    }  
  }  
  
  private fun shortToByte(data: ShortArray): ByteArray {  
    val arraySize = data.size  
    val bytes = ByteArray(arraySize * 2)  
    for (i in 0 until arraySize) {  
      bytes[i * 2] = (data[i].toInt() and 0x00FF).toByte()  
      bytes[i * 2 + 1] = (data[i].toInt() shr 8).toByte()  
      data[i] = 0  
    }  
    return bytes  
  }  
  
  private fun writeAudioFile() {  
    try {  
      val outputStream = FileOutputStream(rawOutput!!.absolutePath)  
      val data = ShortArray(bufferElements2Record)  
  
      while (isRecording) {  
        mAudioRecord!!.read(data, 0, bufferElements2Record)  
  
        val buffer = ByteBuffer.allocate(8 * 1024)  
  
        outputStream.write(  
          shortToByte(data),  
          0,  
          bufferElements2Record * bytesPerElement  
        )  
      }  
  
      outputStream.close()  
    } catch (e: FileNotFoundException) {  
      Log.e(TAG, "File Not Found: $e")  
      e.printStackTrace()  
    } catch (e: IOException) {  
      Log.e(TAG, "IO Exception: $e")  
      e.printStackTrace()  
    }  
  }  
  
  @SuppressLint("SimpleDateFormat")  
  fun startProcessing() {  
    isRecording = false  
    mAudioRecord!!.stop()  
    mAudioRecord!!.release()  
  
    mFileName = SimpleDateFormat("yyyy-MM-dd hh-mm-ss").format(Date()) + ".mp3"  
  
    //Convert To mp3 from raw data i.e pcm  
    val output = File(root, mFileName)  
  
    try {  
      output.createNewFile()  
    } catch (e: IOException) {  
      e.printStackTrace()  
      Log.e(TAG, "startProcessing: $e")  
    }  
  
    try {  
      rawOutput?.let { rawToWave(it, output) }  
    } catch (e: IOException) {  
      e.printStackTrace()  
    } finally {  
      rawOutput!!.delete()  
    }  
  }  
  
  private fun stop(){  
    startProcessing()  
    if (mAudioRecord != null){  
      mAudioRecord = null  
      recordingThread = null  
    }  
  }  
  
  override fun onDetachedFromEngine(binding: FlutterPlugin.FlutterPluginBinding) {}  
  
  override fun onAttachedToActivity(binding: ActivityPluginBinding) {  
    activityBinding = binding;  
    channel = MethodChannel(pluginBinding!!.binaryMessenger, "system_audio_recorder")  
    channel.setMethodCallHandler(this)  
    activityBinding!!.addActivityResultListener(this);  
  }  
  
  override fun onDetachedFromActivityForConfigChanges() {}  
  
  override fun onReattachedToActivityForConfigChanges(binding: ActivityPluginBinding) {  
    activityBinding = binding;  
  }  
  
  override fun onDetachedFromActivity() {}  
}
```



此外需要配置一下 `system_audio_recorder/src/main/AndroidManifest.xml`，添加一些权限。

```xml
<?xml version="1.0" encoding="utf-8"?>  
<manifest xmlns:android="http://schemas.android.com/apk/res/android"  
    package="com.example.system_audio_recorder">  
  
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />  
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />  
    <uses-permission android:name="android.permission.WRITE_INTERNAL_STORAGE" />  
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />  
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PROJECTION" />  
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_TYPE_MEDIA_PROJECTION" />  
    <uses-permission android:name="android.permission.WAKE_LOCK" />  
    <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />  
    <uses-permission android:name="android.permission.RECORD_AUDIO" />  
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />  
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PROJECTION" />  
  
</manifest>
```

#### 插件代码

接下来使用 android studio 打开 system_audio_recorder，编写插件代码。

首先配置一下 `system_audio_recorder/pubspec.yaml`，添加 dependencies

```yaml
dependencies:  
  flutter:  
    sdk: flutter  
  plugin_platform_interface: ^2.0.2 
  # 新添加的dependencies
  flutter_foreground_task: ^6.0.0+1  
  meta: ^1.5.0
```

在 `system_audio_recorder/lib` 中有三个 dart 文件，三个文件的内容为

`system_audio_recorder/lib/system_audio_recorder.dart`

```dart
  
import 'dart:ffi';  
import 'dart:io';  
  
import 'package:flutter/foundation.dart';  
  
import 'system_audio_recorder_platform_interface.dart';  
import 'package:flutter_foreground_task/flutter_foreground_task.dart';  
  
class SystemAudioRecorder {  
  Future<String?> getPlatformVersion() {  
    return SystemAudioRecorderPlatform.instance.getPlatformVersion();  
  }  
  static Future<bool> startRecord(String name, {String? titleNotification, String? messageNotification, int? sampleRate}) async {  
    try {  
      if (titleNotification == null) {  
        titleNotification = "";  
      }  
      if (messageNotification == null) {  
        messageNotification = "";  
      }  
  
      if (sampleRate == null){  
        sampleRate = 44100;  
      }  
  
      await _maybeStartFGS(titleNotification, messageNotification);  
      final bool start = await SystemAudioRecorderPlatform.instance.startRecord(  
        name,  
        notificationTitle: titleNotification,  
        notificationMessage: messageNotification,  
        sampleRate: sampleRate,  
      );  
  
      return start;  
    } catch (err) {  
      print("startRecord err");  
      print(err);  
    }  
  
    return false;  
  }  
  
  static Future<String> get stopRecord async {  
    try {  
      final String path = await SystemAudioRecorderPlatform.instance.stopRecord;  
      if (!kIsWeb && Platform.isAndroid) {  
        FlutterForegroundTask.stopService();  
      }  
      return path;  
    } catch (err) {  
      print("stopRecord err");  
      print(err);  
    }  
    return "";  
  }  
  
  static _maybeStartFGS(String titleNotification, String messageNotification) {  
    try {  
      if (!kIsWeb && Platform.isAndroid) {  
        FlutterForegroundTask.init(  
          androidNotificationOptions: AndroidNotificationOptions(  
            channelId: 'notification_channel_id',  
            channelName: titleNotification,  
            channelDescription: messageNotification,  
            channelImportance: NotificationChannelImportance.LOW,  
            priority: NotificationPriority.LOW,  
            iconData: const NotificationIconData(  
              resType: ResourceType.mipmap,  
              resPrefix: ResourcePrefix.ic,  
              name: 'launcher',  
            ),  
          ),  
          iosNotificationOptions: const IOSNotificationOptions(  
            showNotification: true,  
            playSound: false,  
          ),  
          foregroundTaskOptions: const ForegroundTaskOptions(  
            interval: 5000,  
            autoRunOnBoot: true,  
            allowWifiLock: true,  
          ),  
        );  
      }  
    } catch (err) {  
      print("_maybeStartFGS err");  
      print(err);  
    }  
  }  
}
```


`system_audio_recorder_method_channel.dart`

```dart
import 'package:flutter/foundation.dart';  
import 'package:flutter/services.dart';  
  
import 'system_audio_recorder_platform_interface.dart';  
  
/// An implementation of [SystemAudioRecorderPlatform] that uses method channels.  
class MethodChannelSystemAudioRecorder extends SystemAudioRecorderPlatform {  
  /// The method channel used to interact with the native platform.  
  @visibleForTesting  
  final methodChannel = const MethodChannel('system_audio_recorder');  
  
  @override  
  Future<String?> getPlatformVersion() async {  
    final version = await methodChannel.invokeMethod<String>('getPlatformVersion');  
    return version;  
  }  
  
  Future<bool> startRecord(  
      String name, {  
        String notificationTitle = "",  
        String notificationMessage = "",  
        int sampleRate = 44100  
      }) async {  
    final bool start = await methodChannel.invokeMethod('startRecord', {  
      "name": name,  
      "title": notificationTitle,  
      "message": notificationMessage,  
      "sampleRate": sampleRate  
    });  
    return start;  
  }  
  
  
  Future<String> get stopRecord async {  
    final String path = await methodChannel.invokeMethod('stopRecord');  
    return path;  
  }  
}
```

`system_audio_recorder_platform_interface.dart`

```dart
import 'package:plugin_platform_interface/plugin_platform_interface.dart';  
  
import 'system_audio_recorder_method_channel.dart';  
  
abstract class SystemAudioRecorderPlatform extends PlatformInterface {  
  /// Constructs a SystemAudioRecorderPlatform.  
  SystemAudioRecorderPlatform() : super(token: _token);  
  
  static final Object _token = Object();  
  
  static SystemAudioRecorderPlatform _instance = MethodChannelSystemAudioRecorder();  
  
  /// The default instance of [SystemAudioRecorderPlatform] to use.  
  ///  /// Defaults to [MethodChannelSystemAudioRecorder].  
  static SystemAudioRecorderPlatform get instance => _instance;  
  
  /// Platform-specific implementations should set this with their own  
  /// platform-specific class that extends [SystemAudioRecorderPlatform] when  
  /// they register themselves.  
  static set instance(SystemAudioRecorderPlatform instance) {  
    PlatformInterface.verifyToken(instance, _token);  
    _instance = instance;  
  }  
  
  Future<String?> getPlatformVersion() {  
    throw UnimplementedError('platformVersion() has not been implemented.');  
  }  
  Future<bool> startRecord(  
      String name, {  
        String notificationTitle = "",  
        String notificationMessage = "",  
        int sampleRate = 44100  
      }) {  
    throw UnimplementedError();  
  }  
  
  Future<String> get stopRecord {  
    throw UnimplementedError();  
  }  
}
```


#### example 代码

最后用 android studio 打开 `system_audio_recorder/example` 文件夹，这里需要在 `system_audio_recorder/example/android/app/src/main/AndroidManifest.xml` 中添加 service

```xml
<application  
    android:label="system_audio_recorder_example"  
    android:name="${applicationName}"  
    android:icon="@mipmap/ic_launcher"> 
     
	<!--添加service-->
    <service  
        android:name="com.foregroundservice.ForegroundService"  
        android:foregroundServiceType="mediaProjection"  
        android:enabled="true"  
        android:exported="false">  
    </service>  
    
    <activity  
        android:name=".MainActivity"
        .....
```

同时修改 `system_audio_recorder\example\android\app\build.gradle` 中的 minSdkVersion 为 23

最后在 `main.dart` 中编写开始录音和停止录音的代码即可

```dart
import 'package:flutter/foundation.dart';  
import 'package:flutter/material.dart';  
import 'dart:async';  
  
import 'package:flutter/services.dart';  
import 'package:system_audio_recorder/system_audio_recorder.dart';  
import 'package:permission_handler/permission_handler.dart';  
  
void main() {  
  runApp(const MyApp());  
}  
  
class MyApp extends StatefulWidget {  
  const MyApp({super.key});  
  
  @override  
  State<MyApp> createState() => _MyAppState();  
}  
  
class _MyAppState extends State<MyApp> {  
  String _platformVersion = 'Unknown';  
  final _systemAudioRecorderPlugin = SystemAudioRecorder();  
  requestPermissions() async {  
    if (!kIsWeb) {  
      if (await Permission.storage.request().isDenied) {  
        await Permission.storage.request();  
      }  
      if (await Permission.photos.request().isDenied) {  
        await Permission.photos.request();  
      }  
      if (await Permission.microphone.request().isDenied) {  
        await Permission.microphone.request();  
      }  
    }  
  }  
  @override  
  void initState() {  
    super.initState();  
    requestPermissions();  
    initPlatformState();  
  }  
  
  // Platform messages are asynchronous, so we initialize in an async method.  
  Future<void> initPlatformState() async {  
    String platformVersion;  
    // Platform messages may fail, so we use a try/catch PlatformException.  
    // We also handle the message potentially returning null.    try {  
      platformVersion =  
          await _systemAudioRecorderPlugin.getPlatformVersion() ?? 'Unknown platform version';  
    } on PlatformException {  
      platformVersion = 'Failed to get platform version.';  
    }  
  
    // If the widget was removed from the tree while the asynchronous platform  
    // message was in flight, we want to discard the reply rather than calling    // setState to update our non-existent appearance.    if (!mounted) return;  
  
    setState(() {  
      _platformVersion = platformVersion;  
    });  
  }  
  
  @override  
  Widget build(BuildContext context) {  
    return MaterialApp(  
      home: Scaffold(  
        appBar: AppBar(  
          title: const Text('Plugin example app'),  
        ),  
        body: Column(  
          children: [  
            Text('Running on: $_platformVersion\n'),  
            TextButton(onPressed: () async {  
              bool start = await SystemAudioRecorder.startRecord("test",  
              titleNotification: "titleNotification",  
                messageNotification: "messageNotification",  
                sampleRate: 16000  
              );  
            }, child: const Text("开始录制")),  
            TextButton(onPressed: ()async{  
              String path = await SystemAudioRecorder.stopRecord;  
              print(path);  
            }, child: const Text("停止录制"))  
          ]  
        ),  
      ),  
    );  
  }  
}
```


#### 注意问题

如果遇到 java.lang.SecurityException: Media projections require a foreground service of type ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PROJECTION 这种错误时，如果确保已经添加权限，可能需要看一下 ForegroundService 的包名是否和插件的包名一致，如果一致，需要修改 ForegroundService 的包名，否则会报错。


### 从 Java 中回传数据

使用 EventChannel 可以从 java 中回传数据，以此来实现监听流的效果。

#### 原生代码

在原生代码中需要声明

```kotlin
private var eventSink: EventSink? = null
private var binaryMessenger: BinaryMessenger? = null
```

在 `onAttachedToEngine` 函数中赋值 binaryMessenger

```kotlin
binaryMessenger = flutterPluginBinding.binaryMessenger;
```

在重载的方法调用函数 `onMethodCall` 设置监听函数

```kotlin
EventChannel(binaryMessenger, "system_audio_recorder/audio_stream").setStreamHandler(
    object : StreamHandler {
        override fun onListen(args: Any, events: EventSink?) {
            Log.i(TAG, "Adding listener")
            eventSink = events
        }

        override fun onCancel(args: Any) {
            eventSink = null
        }
    }
)
```

在需要传数据的地方执行 `eventSink.success(data)`，不过可能会遇到  java.lang.RuntimeException: Methods marked with @UiThread must be executed on the main thread. 这个问题，需要采用下面的代码

```kotlin
activityBinding!!.activity.runOnUiThread{
  eventSink?.success(byte)
}
```

activityBinding 可以在 onAttachedToActivity 函数中赋值

```kotlin
private var activityBinding: ActivityPluginBinding? = null;

override fun onAttachedToActivity(binding: ActivityPluginBinding) {
    activityBinding = binding;
    activityBinding!!.addActivityResultListener(this);
}
override fun onDetachedFromActivityForConfigChanges() {}
override fun onReattachedToActivityForConfigChanges(binding: ActivityPluginBinding) {
    activityBinding = binding;
}
override fun onDetachedFromActivity() {}
```

注意 onAttachedToActivity 和 onReattachedToActivityForConfigChanges 需要让插件类额外继承 import io.flutter.plugin.common.PluginRegistry.ActivityResultListener 和 ActivityAware

#### 插件代码

定义一个 EventChannel 静态变量即可

```dart
static const EventChannel audioStream = EventChannel('system_audio_recorder/audio_stream');
```


#### example 代码

声明一个流订阅

```dart
StreamSubscription? _audioSubscription;
```

定义流订阅

```dart
if(_audioSubscription == null){
    _audioSubscription = SystemAudioRecorder.audioStream.receiveBroadcastStream({"config": "null"}).listen((data){
        // print("${data.length}");
        allData.addAll(data);
    });
}
```

这里的 receiveBroadcastStream 中需要配置参数，否则会报错。



## 基于 C++ 插件开发

[向您的项目添加 C 和 C++ 代码  | Android Studio  | Android Developers](https://developer.android.google.cn/studio/projects/add-native-code?hl=zh-cn)

一个示例插件：[Xiang-M-J/flutter_jni_plugin_example](https://github.com/Xiang-M-J/flutter_jni_plugin_example)

一些功能可能难以使用 `Java/Kotlin` 编写，如某些硬件可能只提供了 C++ 库作为操作接口，为了调用这些库，可以考虑使用 JNI 技术在 Java 中调用 C++/C。


### 基本知识


在 Android Studio 中新建一个 Native C++ 项目 `test_jni`，默认情况下在 `test_jni\android\app\src\main` 目录下有 `cpp`、`java` 和 `res` 三个文件夹，其中 `res` 文件夹不需要管，`cpp` 文件夹用于存放 C++ 程序，其中有 `CMakeLists.txt` 用于指定编译的文件，`native-lib.cpp` 中为 jni 的接口函数。 `java` 文件夹用来存放调用 jni 程序的代码。

`CMakeLists.txt` 的内容如下

```cmake
cmake_minimum_required(VERSION 3.22.1)

project("test_jni")

add_library(${CMAKE_PROJECT_NAME} SHARED
        # List C/C++ source files with relative paths to this CMakeLists.txt.
        native-lib.cpp)

target_link_libraries(${CMAKE_PROJECT_NAME}
        # List libraries link to the target library
        android
        log)
```


`native-lib.cpp` 的内容如下

```cpp
#include <jni.h>
#include <string>

extern "C" JNIEXPORT jstring JNICALL
Java_com_example_test_1jni_MainActivity_stringFromJNI(
        JNIEnv* env,
        jobject /* this */) {
    std::string hello = "Hello from C++";
    return env->NewStringUTF(hello.c_str());
}
```

`MainActivity.kt` 的内容如下

```kotlin
class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Example of a call to a native method
        binding.sampleText.text = stringFromJNI()
    }

    external fun stringFromJNI(): String

    companion object {
        // Used to load the 'test_jni' library on application startup.
        init {
            System.loadLibrary("test_jni")
        }
    }
}
```


此外在 `test_jni\android\app\build.gradle` 中添加了指定 `CMakeLists.txt` 的配置

```json
android{
    externalNativeBuild {
        cmake {
            path file('src/main/cpp/CMakeLists.txt')
            version '3.22.1'
        }
    }
}
```


上面的内容可以直接移植到其它项目，如 flutter 插件项目。

如果 `C++` 中调用了一些链接库， 可以在 `test_jni\android\app\src\main` 目录下创建 `jniLibs` 文件夹存放这些链接库，一般是 `.so` 文件。`jniLibs` 文件夹的结构一般如下


```
jniLibs
	- arm64-v8a
		- librknnrt.so
	- armeabi-v7a
		- librknnrt.so
```

然后在 `CMakeLists.txt` 中的 `target_link_libraries` 添加链接库路径（具体根据实际情况来定）

```cmake
cmake_minimum_required(VERSION 3.22.1)

project("test_rknn")

add_library(${CMAKE_PROJECT_NAME} SHARED
        # List C/C++ source files with relative paths to this CMakeLists.txt.
        native-lib.cpp
        model.cpp
        model.h
        Float16.h
)

target_link_libraries(${CMAKE_PROJECT_NAME}
        # List libraries link to the target library
        android
        log
        ${CMAKE_SOURCE_DIR}/../jniLibs/${CMAKE_ANDROID_ARCH_ABI}/librknnrt.so
)
```


然后在 `import_rknn\android\build.gradle` 中指定 `C/C++` 的编译方式，如果使用的链接库仅支持部分架构，可以添加架构过滤器。

```json
android {
    // ...

    defaultConfig {
        minSdk = 21
        ndk {
            abiFilters 'armeabi-v7a', 'arm64-v8a' // 仅构建所需的架构
        }
    }
	// ...

    externalNativeBuild {  // 指定 CMakeLists.txt
        cmake {
            path file('src/main/cpp/CMakeLists.txt')
            version '3.22.1'
        }
    }
}

```

> [!NOTE] 
>
> 如果希望添加新的 `jni` 函数，可以现在 Kotlin 文件中定义函数
>
> 
>
> ```kotlin
> external fun initModel(modelData: ByteArray, modelLength: Int): Boolean
> ```
>
> 然后利用 Android Studio 自带的纠错功能在 native-lib.cpp 中添加函数。


### 常用功能


下面介绍一些 c++ 端的常用功能

#### 日志功能


输出信息和错误的函数（使用 printf 输出不会显示）

```cpp
#include <android/log.h>
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, "rktest", ##__VA_ARGS__);
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, "rktest", ##__VA_ARGS__);


// use
LOGI("hello, %d", 1)
```

#### 数据类型转换


**ByteArray (Kotlin), jbyteArray (jni) 转 uint8_t * (c++)**

```cpp
extern "C"
JNIEXPORT jboolean JNICALL
Java_com_example_import_1rknn_ImportRknnPlugin_initModel(JNIEnv *env, jobject thiz,
                                                         jbyteArray model_data) {
    uint32_t model_len = env->GetArrayLength(model_data);
    LOGI("model length: %d", model_len)
    jbyte* byteArray = env->GetByteArrayElements(model_data, nullptr);

    uint8_t * u8_model_data = new uint8_t [model_len];
    memcpy(u8_model_data, byteArray, model_len);
    env->ReleaseByteArrayElements(model_data, byteArray, JNI_ABORT);
    return init_model(u8_model_data, model_len);
}
```


**FloatArray (Kotlin), jfloatArray (jni) 转 jfloat * (c++)**


```cpp
extern "C"
JNIEXPORT jint JNICALL
Java_com_example_import_1rknn_ImportRknnPlugin_inference(JNIEnv *env, jobject thiz, jfloatArray mic, jfloatArray spec) {
    jboolean inputCopy = JNI_FALSE;
    jboolean outputCopy = JNI_FALSE;

    jfloat * const jmic = env->GetFloatArrayElements(mic, &inputCopy);
    jfloat * const jspec = env->GetFloatArrayElements(spec, &outputCopy);
    
    inference(jmic, jspec);

    env->ReleaseFloatArrayElements(mic, jmic, 0);
    return 0;
}
```


**float * 转 jfloatArray (jni)**

```cpp
float *spec = (float *) malloc(frameSize * sizeof(float ));
jfloatArray jspec = env->NewFloatArray(frameSize);  
env->SetFloatArrayRegion(jspec, 0, frameSize, spec);
```



## build.gradle 任务


### Debug 任务

在 android/app/build.gradle 中

```json

// 复制链接
task copyMergedNativeLibs(type: Copy){
    from "../../native-libs/libs/"
    include "*/*.so"
    into "../../build/app/intermediates/merged_native_libs/debug/out/lib/"
}

// 复制链接
task copyStrippedNativeLibs(type: Copy){
    from "../../native-libs/libs/"
    include "*/*.so"
    into "../../build/app/intermediates/merged_native_libs/debug/out/lib/"
}

// 清理文件
task cleanTempFiles(type: Delete) {
    delete fileTree(dir: '../../build/app/intermediates/flutter/debug/flutter_assets/assets', include: '*.onnx')
}

preBuild.dependsOn copyMergedNativeLibs
preBuild.dependsOn copyStrippedNativeLibs
preBuild.dependsOn cleanTempFiles
```

### release 任务

```json

task preReleaseBuildTask{

    delete fileTree(dir: '../../build/app/intermediates/flutter/release/flutter_assets/assets', include: '*.onnx')
    copy{
        from ("../../native-libs/libs/")
        include ("*/*.so")
        into ("../../build/app/intermediates/merged_native_libs/release/out/lib/")
    }
    copy{
        from ("../../native-libs/libs/")
        include ("*/*.so")
        into ("../../build/app/intermediates/merged_native_libs/release/out/lib/")
    }
}

tasks.whenTaskAdded { task ->
    if (task.name == 'assembleRelease') {
        task.dependsOn preReleaseBuildTask
    }
}

```

## 编写链接库

### flutter 端

一般使用 C/C++ 编写链接库，C/C++端只需要按照一般的情况去编写代码即可，尽量不去引用其它库。

为了将 C/C++ 文件编译成适合 Android 平台的链接库，需要创建一个 CMake 项目

```cmake
# The Flutter tooling requires that developers have CMake 3.10 or later
# installed. You should not increase this version, as doing so will cause
# the plugin to fail to compile for some customers of the plugin.
cmake_minimum_required(VERSION 3.10)

project(stft_qmf_library VERSION 0.0.1 LANGUAGES C)

# 函数实现
add_library(stft_qmf SHARED
  "qmf.c" "stft.c"
)

# 在 spl.h 中定义好所有需要用到的函数
set_target_properties(stft_qmf PROPERTIES
  PUBLIC_HEADER spl.h  
  OUTPUT_NAME "stft_qmf"
)

target_compile_definitions(stft_qmf PUBLIC DART_SHARED_LIB)
```

此外需要创建 `Android.mk` 和 `Application.mk`

**Android.mk**

```makefile
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)

LOCAL_MODULE := libSpl
LOCAL_C_INCLUDES := qmf.h spl.h
LOCAL_SRC_FILES := qmf.c stft.c

LOCAL_LDLIBS := -llog

include $(BUILD_SHARED_LIBRARY)
```

**Application.mk**

```makefile
 APP_ABI := arm64-v8a armeabi-v7a x86 x86_64
```

编写一个脚本来编译

```sh
D:\android-ndk-r26d\build\ndk-build NDK_PROJECT_PATH=. NDK_APPLICATION_MK=Application.mk APP_BUILD_SCRIPT=Android.mk
```


如果不想手动复制链接，可以在 `android/app/build.gradle` 中定义复制任务，先在项目根目录下创建一个 native-libs 文件夹，再将链接库放在其中

```json
task copyMergedNativeLibs(type: Copy){  
    from "../../native-libs/libs/"  
    include "*/*.so"  
    into "../../build/app/intermediates/merged_native_libs/debug/out/lib/"  
}  
  
task copyStrippedNativeLibs(type: Copy){  
    from "../../native-libs/libs/"  
    include "*/*.so"  
    into "../../build/app/intermediates/merged_native_libs/debug/out/lib/"  
}  
  
preBuild.dependsOn copyMergedNativeLibs  
preBuild.dependsOn copyStrippedNativeLibs
```


### 链接库的一些说明

如果需要重复调用一段程序，并且存在一些状态值，如使用数组 `x` 保存之前运算的部分结果，不需要每次都将 `x` 传入程序，而是直接在程序中定义即可，如

```c
short x[NUM] = { 0 };

void process(short *in, float *out){
	memcpy(&x[NUM / 2], in, sizeof(short) * NUM / 2);
	for(int i=0; i<NUM; i++){
		out[i] = in[i] * 2;
	}
}
```

上面这段程序让 `x` 保留输入的后 `NUM/2` 点数据，直接定义 `x` 并在函数中修改即可，在应用运行时，`x` 的状态会一直保持并更新。

如果需要开始一次新的计算，可以编写一个重置函数来重置 `x`

```c
void reset(){
	memset(&x, 0, sizeof(short) * NUM);
}
```

## 入门知识

### 基本命令

`flutter doctor`：检查一下 `flutter` 环境是否有问题

`flutter create project_name`：新建项目工程（只能小写）

```cmd
cd project_name
flutter run
```

`flutter pub add <package>`：添加包


flutter 构建 App，在项目路径下执行

```powershell
flutter build apk
```

flutter 编译 web 应用

```sh
flutter build web
```

使用 --web-renderer 选择使用 html 或是 canvaskit 渲染

```sh
flutter build web --web-renderer html
```

在默认选项下以发行模式构建

```sh
flutter build web --release
```

### 基本知识

`flutter` 是跨平台的，一套代码适用于 ios、Android、web、Macos、Linux 和 windows。对于不需要的平台，可以直接删除文件夹。

`pubspec.yaml` 文件中声明了依赖、flutter 使用的资源

## 控件

**flutter 中可以放置多个控件的容器**：

1. [Row](https://api.flutter.dev/flutter/widgets/Row-class.html) 和 [Column](https://api.flutter.dev/flutter/widgets/Column-class.html)
2. [GridView](https://api.flutter.dev/flutter/widgets/GridView-class.html)
3. [ListView](https://api.flutter.dev/flutter/widgets/ListView-class.html)
4. [Stack](https://api.flutter.dev/flutter/widgets/Stack-class.html)
5. [Flex](https://api.flutter.dev/flutter/widgets/Flex-class.html) + [Expanded](https://api.flutter.dev/flutter/widgets/Expanded-class.html) 实现弹性窗口
6. [Wrap](https://api.flutter.dev/flutter/widgets/Wrap-class.html)


**可以用来占位调节位置的组件**：

Container 直接放在两个元素之间：

```dart
Container(height: 30,),
```

Padding 将元素包裹起来：

```dart
Padding(
    padding: const EdgeInsets.all(20),
    child: ListTile(
      title: Text("${list[index]}"),
    ),
)
```

SizedBox 放在两个元素之间

```dart
const SizedBox(height: 10),
```


### 两种窗口

flutter 中有 `StatelessWidget` 和 `StatefulWidget`，顾名思义，`StatelessWidget` 是一个不需要状态更改的 widget（没有要管理的内部状态），当界面部分不依赖于对象本身中的配置信息以及 widget 的 `BuildContext` 时，可以使用 `StatelessWidget`。`StatefulWidget` 是可变状态的 widget。 使用 `setState` 方法管理 `StatefulWidget` 的状态的改变。调用 `setState` 告诉 Flutter 框架，某个状态发生了变化，Flutter 会重新运行 build 方法，以便应用程序可以应用最新状态。

如果用户与 widget 交互，widget 会发生变化，那么它就是 **有状态的**。

```dart
// StatelessWidget
import 'package:flutter/material.dart';

class MyStatelessWidget extends StatelessWidget {

  MyStatelessWidget({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text(
        "hello",
        textDirection: TextDirection.ltr,
      ),
    );
  }
}

// StatefulWidget
class MyStatefulWidget extends StatefulWidget {
  MyStatefulWidget({super.key});
  @override
  _MyStatefulWidgetState createState() => _MyStatefulWidgetState();
}

class _MyStatefulWidgetState extends State<MyStatefulWidget> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text(
        "hello",
        textDirection: TextDirection.ltr,
      ),
    );
  }
```


### 控件的组合

在 flutter 中，如果希望在一个界面放置多个控件，需要使用 `Row`、`Column` 等包装起来：

```dart
return Scaffold(
      body: Center(
        child: Column(
          children: [
            const Spacer(),
            ElevatedButton(
              style: ButtonStyle(
                textStyle: MaterialStateProperty.all(const TextStyle(fontSize: 24))
              ),
              onPressed: (){
                Navigator.of(context).push(_createRoute());
              },
              child: const Text("A"),
            ),
            const Spacer(),
            ElevatedButton(
              style: ButtonStyle(
                textStyle: MaterialStateProperty.all(const TextStyle(fontSize: 24))
              ),
              onPressed: (){
                Navigator.of(context).push(MaterialPageRoute(builder: (context) => PhysicsCardDrag()));
              }, 
              child: const Text("B")
            ),
            const Spacer()
          ]
        ) 
      )
    );
```

> 使用 `const spacer()` 可以自动排列控件。

### AppBar

如果需要界面上面存在返回键，可以加上 `appBar: AppBar(),`

```dart
class Page extends StatelessWidget{
  const Page({super.key});
  @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: AppBar(
      	title: const Text("AppBar"),
      ),
      body: const Center(
        child: Text("Page"),
      ),
    );
  }
}
```

### Drawer 左侧菜单

> 注意当 AppBar 和 Drawer 同时存在时，屏幕不会出现返回键。

可以先定义左侧菜单类 MyDrawer：

```dart
class MyDrawer extends StatelessWidget {
  const MyDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      elevation: 16.0,
      child: ListView
      (children: <Widget>[
          UserAccountsDrawerHeader(
            accountName: Text(User.username),
            accountEmail: Text(User.email),
            currentAccountPicture: const CircleAvatar(
              backgroundImage: AssetImage("assets/images/userIcon.jpg"),
            ),
            decoration: const BoxDecoration(
              image: DecorationImage(
                  image: AssetImage("assets/images/userBg.jpg"),
                  fit: BoxFit.cover),
            ),
          ),
          const ListTile(
            leading: Icon(Icons.settings),
          ),
          const Divider(),
          const ListTile(
            leading: Icon(Icons.language),
          ),
        ],
      ),
    );
  }
}
```

在 main.dart 中的 _MyHomePageState 的 Scaffold 类的 drawer 属性中设置：

```dart
class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Body(),
      drawer: MyDrawer(),
    );
  }
}
```

设置之后可以通过下面的命令弹出左侧窗口（关闭左侧窗口是默认操作）：

```dart
Scaffold.of(context).openDrawer();
```

### TabBar 选项卡

选项卡 TabBar，放在 AppBar 中，在非 MaterialApp 的环境下不会影响返回键的显示

```dart
Widget build(BuildContext context) {
    return MaterialApp(
      home: DefaultTabController(
        length: 3,
        child: Scaffold(
          appBar: AppBar(
            bottom: const TabBar(tabs: [
              Tab(icon: Icon(Icons.directions_car)),
              Tab(icon: Icon(Icons.directions_train)),
              Tab(icon: Icon(Icons.directions_bike)),
            ]),
            title: const Text("Tabs"),
          ),
          body: const TabBarView(children: [
            Icon(Icons.directions_car),
            Icon(Icons.directions_train),
            Icon(Icons.directions_bike)
          ]),
        ),
      ),
    );
  }
```

### Container 容器

```dart
Container(
  height: 200,
  width: 200,
  decoration: const BoxDecoration(
    color: Color.fromARGB(255, 11, 158, 158)
  ),
  alignment: Alignment.center,
  child: const Text(
    "Hello World",
    style: TextStyle(fontSize: 20),
  ),
)
```

double.infinity 和 double.maxFinite 可以让当前元素的 width 或者 height 达到父元素的尺寸

### 动态列表

使用 for 实现动态列表

```dart
class DynamicList extends StatelessWidget{
  const DynamicList({super.key});

  List<Widget> _initListView(){
    List<Widget> list = [];
    for (int i = 0; i < 10; i++) {
      list.add(Text("列表：$i"));
    }
    return list;
  }
  @override
  Widget build(BuildContext context){
    return ListView(
      children: _initListView(),
    );
  }
}
```

使用 ListView.builder 实现动态列表（实例化该页面时不能使用 const 修饰）

```dart
class DynamicList extends StatelessWidget {
  List list = [];
  DynamicList({Key? key}) : super(key: key) {
    for (var i = 0; i < 10; i++) {
      list.add("我是一个列表--$i");
    }
  }
  @override
  Widget build(BuildContext context) {
    return Material(child:  ListView.builder(
        itemCount: list.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text("${list[index]}"),
          );
        })) ;
  }
}
```

动态列表往往容易溢出高度，可以使用 Flexible 组件包裹：

```dart
Flexible(
    child: ListView.builder(
        controller: _controller,
        itemCount: items.length,
        itemBuilder: (context, index) {
            return ListTile(
            	title: Text(items[index]),
            );
        },
    ),
),
```

### BottomNavigationBar 底部导航

```dart
import 'package:flutter/material.dart';

class BottomNavigation extends StatelessWidget {
  const BottomNavigation({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Navigation",
      theme: ThemeData(primarySwatch: Colors.amber),
      home: const Tabs()
    );
  }
}

class Tabs extends StatefulWidget {
  const Tabs({super.key});
  State<Tabs> createState() => _TabsState();
}

class _TabsState extends State<Tabs>{
  int _currentIndex = 0;
  @override
  Widget build(BuildContext context){
    return Scaffold(
        appBar: AppBar(
          title: const Text("App"),
        ),
        body: const Center(
          child: Text("body"),
        ),
        // 底部导航
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _currentIndex,
          onTap: (value){
            setState(() {
              _currentIndex = value;
            });
          },
          items: const [
            BottomNavigationBarItem(icon: Icon(Icons.home), label: "首页"),
            BottomNavigationBarItem(icon: Icon(Icons.category), label: "分类"),
            BottomNavigationBarItem(icon: Icon(Icons.settings), label: "设置")
          ],
        ),
      );
  }
}
```

### Toast

使用 fluttertoast 插件，显示 toast 的代码：

```dart
Fluttertoast.showToast(
    msg: "Detail",
    toastLength: Toast.LENGTH_SHORT,
    gravity: ToastGravity.CENTER,
    timeInSecForIosWeb: 1,
    backgroundColor: Colors.red,
    textColor: Colors.white,
    fontSize: 16.0
);
```

### 弹出列表菜单 PopupMenuButton

```dart
class Mymenu extends StatelessWidget {
  const Mymenu({super.key});

  List<PopupMenuEntry<String>> _getItemBuilder() {
    return <PopupMenuEntry<String>>[
      const PopupMenuItem<String>(
          child: ListTile(
        leading: Icon(Icons.share),
        title: Text("分享"),
      )),
      const PopupMenuDivider(),
      const PopupMenuItem<String>(
          child: ListTile(
        leading: Icon(Icons.update),
        title: Text("更新"),
      ))
    ];
  }

  @override
  Widget build(BuildContext context) {
    return PopupMenuButton(
      itemBuilder: (BuildContext context) {
        return _getItemBuilder();
      },
      icon: const Icon(Icons.menu),
      onSelected: (value) {
        print(value);
      },
      onCanceled: () {},
      offset: const Offset(100, 50),
    );
  }
}
```

### floatingActionButton 悬浮按钮

一般在 Scaffold 类中使用，可以实现一键回到顶端的功能。

```dart
class BodyState extends State<Body> {
  // 设置控件控制按钮的显示
  final ScrollController _controller = ScrollController(keepScrollOffset: false);
  bool shown = false;

  @override
  void initState() {
    super.initState();
    _controller.addListener(isScroll);
  }
  @override
  void dispose() {
    super.dispose();
    _controller.removeListener(isScroll);
  }
  
  void isScroll() {
    final bool toShow = (_controller.offset ?? 0) > MediaQuery.of(context).size.height / 2;
    shown = toShow ? true : false;
    setState(() {});
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        ...
      ),
       floatingActionButton: !shown ? null : FloatingActionButton(
        onPressed: () {
          _controller.animateTo(0,
              duration: const Duration(milliseconds: 400),
              curve: Curves.easeIn);
        },
        tooltip: "一键回到顶端",
        child: const Icon(Icons.arrow_upward),
      ),
    );
  }
}
```


## 动画

### 循环播放

[Flutter Animation 动画开发之——repeat 循环播放_flutter 循环动画-CSDN 博客](https://blog.csdn.net/mqdxiaoxiao/article/details/102933512)

循环播放一个圆从小到大，同时改变颜色。

```dart
import 'package:flutter/material.dart';

class RepeatAnimationWidget extends StatelessWidget {
  const RepeatAnimationWidget({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      home: const RepeatAnimation(),
    );
  }
}
class RepeatAnimation extends StatefulWidget {
  const RepeatAnimation({super.key});
  @override
  State<RepeatAnimation> createState() => _RepeatAnimation();
}
class _RepeatAnimation extends State<RepeatAnimation> with SingleTickerProviderStateMixin {
  late Animation<double> animation;   // 宽和高的动画
  late Animation<Color?> animationC;  // 颜色的动画
  late AnimationController controller;
  String text = "停止";
  @override
  initState() {
    super.initState();
    // Controller设置动画时长
    // vsync设置一个TickerProvider，当前State 混合了SingleTickerProviderStateMixin就是一个TickerProvider
    controller = AnimationController(
        duration: const Duration(seconds: 2),
        vsync: this );
    // Tween设置动画的区间值，animate()方法传入一个Animation，AnimationController继承Animation
    animation = Tween(begin: 100.0, end: 200.0).animate(controller);
    animationC = ColorTween(begin: Colors.blueAccent, end: Colors.amber).animate(controller);
    controller.repeat();   // 循环播放
//    controller.repeat(reverse: true);  // 循环往返播放
  }
  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
        animation: Listenable.merge([animation, animationC]),  // 合并两个动画
        builder: (BuildContext ctx, Widget? child) {
          return Center(
            child: Container(
              alignment: Alignment.center,
              width: animation.value,
              height: animation.value,
              decoration: BoxDecoration(
                color: animationC.value,
                borderRadius: BorderRadius.circular(animation.value)
              ),
              child: FloatingActionButton(
                  onPressed: (){
                    if (controller.isAnimating) {
                      controller.stop();
                      setState(() { text = "开始"; });
                    }else{
                      controller.repeat();
                      setState(() { text = "停止";  });
                    }      
                  },
                  child: Text(text)
              ),
            ),
          );
        }
    );
  }
  @override
  void dispose() {
    // 释放资源
    controller.dispose();
    super.dispose();
  }
}
```

## 跳转

### 窗口跳转

如果希望跳转至另外一个窗口（PhysicsCardDrag），可以使用下面的方式

```dart
onPressed: () {
            Navigator.of(context).push(
                MaterialPageRoute(builder: (context) => const Page()));
          },
```

如果希望返回上一个页面，使用下面的方式：

```dart
onPressed: () {
            Navigator.of(context).pop(context);
          },
```

当存在许多页面进行跳转时，可以使用单独的路由文件进行跳转，首先创建一个 `routes.dart`：

```dart
final Map<String, Function> routes = {
  "/": (context,) => const MyHomePage(title: "Flutter Demo"),
  "/drawer": (context, {arguments}) => drawerWidget(title: arguments['title']),
  "/todo": (context) => const todosScreen(),
  "/Bottom": (context) => const BottomNavigation(),
  "/decorate": (context) => const DecorateText(),
  "/list": (context) => DynamicList(),
  "/physics": (context) => const PhysicsCardDrag(),
  "/snack": (context) => const snackBarWidget(),
  "/tab": (context) => const tabBarWidget()
};

var onGenerateRoute = (RouteSettings settings) {
  final String? name = settings.name;
  final Function? pageContentBuilder = routes[name];
  if (pageContentBuilder != null) {
    if (settings.arguments != null) {
      final Route route = MaterialPageRoute(
          builder: (context) =>
              pageContentBuilder(context, arguments: settings.arguments));
      return route;
    } else {
      final Route route =
          MaterialPageRoute(builder: (context) => pageContentBuilder(context));
      return route;
    }
  }
  return null;
};
```

然后在 `main.dart` 中，修改为

```dart
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'App1',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
            seedColor: const Color.fromRGBO(0, 107, 123, 1)),
        useMaterial3: true,
      ),
      initialRoute: "/",
      onGenerateRoute: onGenerateRoute,
    );
  }
}
```

跳转至某个页面：

```dart
Navigator.pushNamed(context, "/drawer", arguments: {
"title": "hello"
}); // 带参数
Navigator.pushNamed(context, "/snack");  // 不带参数
```

替换路由

```dart
Navigator.of(context).pushReplacementNamed('/registerSecond');
```

返回到根路由

```dart
Navigator.of(context).pushAndRemoveUntil(
    MaterialPageRoute(builder: (BuildContext context) {
    	return const HomePage();
    }), (route) => false);
```



### flutter 中的 key

许多组建的构造函数中都会有 key

```dart
const tabBarWidget({super.key});
```

key 的作用是在 Widget tree 中保存状态。对于 `StatelessWidget` 来说，一般不需要指定 key。对于 `StatefulWidget` 来说，当我们想要改变组件时（进行添加、删除、重排序等操作），有时可能没有反应，这时便需要指定 key 了。

```dart
class _ScreenState extends State<Screen> {
  List<Widget> widgets = [
    StatefulContainer(key: UniqueKey(),),
    StatefulContainer(key: UniqueKey(),),
  ];
//  ···
```

详见 [Flutter | 深入浅出 Key - 掘金 (juejin.cn)](https://juejin.cn/post/6844903811870359559)

### 传递数据到新页面

创建一个待办事项列表，当某个事项被点击的时候，会跳转到新的一屏，在新的一屏显示待办事项的详细信息。

> 数据的传递依靠导航窗口时传递参数

```dart
// todosScreen.dart
import 'package:flutter/material.dart';
import 'package:new01/compoents/todo/detailScreen.dart';

class Todo {
  final String title;
  final String description;

  const Todo(this.title, this.description);
}

class todosScreen extends StatelessWidget {
  const todosScreen({super.key});

  static List<Todo> todos = List.generate(
      20,
      (i) => Todo(
          "Todo $i", "A description of what needs to be done for Todo $i"));

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("todos"),
      ),
      body: ListView.builder(
          itemCount: todos.length,
          itemBuilder: (context, index) {
            return ListTile(
              title: Text(todos[index].title),
              onTap: () {
                Navigator.of(context).push(MaterialPageRoute(
                    builder: (context) => detailScreen(todo: todos[index])));
              },
            );
          }),
    );
  }
}
```

```dart
// detailScreen.dart
import 'package:flutter/material.dart';
import 'package:new01/compoents/todo/todosScreen.dart';

class detailScreen extends StatelessWidget {
  const detailScreen({super.key, required this.todo});
  final Todo todo;
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(todo.title),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Text(todo.description),
      ),
    );
  }
}
```

另外一种传递方式：[传递数据到新页面 - Flutter 中文文档 - Flutter 中文开发者网站 - Flutter](https://flutter.cn/docs/cookbook/navigation/passing-data#alternatively-pass-the-arguments-using-routesettings)

### 页面回传数据

通过 `Navigator.pop()` 实现

```dart
import 'package:flutter/material.dart';
...
class _SelectionButtonState extends State<SelectionButton> {
  // 异步
  Future<void> _navigateAndDisplaySelection(BuildContext context) async {
    // 通过 Navigator.pop 回传数据
    final result = await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const SelectionScreen()),
    );

    // 当从StatefulWidget中使用BuildContext时，挂载的属性必须在异步间隙后检查。
    if (!context.mounted) return;

    // 在返回结果之后，隐藏组件并显示新结果。
    ScaffoldMessenger.of(context)
      ..removeCurrentSnackBar()
      ..showSnackBar(SnackBar(content: Text('$result')));
  }
}

class SelectionScreen extends StatelessWidget {
...
      child: ElevatedButton(
        onPressed: () {
          // Close the screen and return "Yep!" as the result.
          Navigator.pop(context, 'Yep!');
        },
        child: const Text('Yep!'),
      ),
...
      child: ElevatedButton(
        onPressed: () {
          // Close the screen and return "Nope." as the result.
          Navigator.pop(context, 'Nope.');
        },
        child: const Text('Nope.'),
      ),
...
```

## 操作

### 添加语音助手

#### 语音合成

使用 flutter_tts 包，[flutter_tts | Flutter package (pub.dev)](https://pub.dev/packages/flutter_tts)

这个包会调用 Android 本地库，所以需要申请对应的权限：

```xml
<queries>
  <intent>
    <action android:name="android.intent.action.TTS_SERVICE" />
  </intent>
</queries>
```

官方给出最小的 SdkVersion 为 21，需要修改 android\app\build.gradle 中的 defaultConfig：

```json
defaultConfig {
        applicationId "com.example.new03"
        // minSdkVersion flutter.minSdkVersion
        minSdkVersion 21 
        targetSdkVersion flutter.targetSdkVersion
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName
    }
```

官方文档给出的关于 flutter_tts 的配置说明存在一些问题，如果写成

```yaml
dependencies:
    flutter:
      sdk: flutter
    flutter_tts:
```

会报错，可能是因为 flutter_tts 对应的 dart 版本不对。如果报错

```txt
[!] Your project requires a newer version of the Kotlin Gradle plugin. │ │ Find the latest version on https://kotlinlang.org/docs/releases.html#release-details, then │ │ update D:\work\app\flutterSample\new03\android\build.gradle: │ │ ext.kotlin_version = '<latest-version>'
```

可以降低版本：

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_tts: ^3.8.5
```

基本用法：

```dart
FlutterTts flutterTts = FlutterTts();
await flutterTts.speak("中午好，今天天气真不错");
```

#### 语音识别

使用 speech_to_text 包，

具体使用参见文档：[speech_to_text - Dart API docs (pub.dev)](https://pub.dev/documentation/speech_to_text/latest/)

相较于语音合成，支持语音识别的浏览器明显较少 ["Web Speech API" | Can I use... Support tables for HTML5, CSS3, etc](https://caniuse.com/?search=Web Speech API)

speech_to_text 要求最小的 SdkVersion 为 21，需要修改 android\app\build.gradle 中的 defaultConfig：

```json
defaultConfig {
        applicationId "com.example.new03"
        // minSdkVersion flutter.minSdkVersion
        minSdkVersion 21 
        targetSdkVersion flutter.targetSdkVersion
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName
    }
```

### flutter 解析 json

使用 http 包获取请求，使用 convert 转换为 json：

```dart
List pokemon = List.empty();

@override
void initState(){
	super.initState();
	fetchData();
}
Future<void> fetchData() async {
    final response = await http.get(Uri.parse('https://raw.githubusercontent.com/Biuni/PokemonGO-Pokedex/master/pokedex.json'));
    if (response.statusCode == 200) {
      Map<String, dynamic> jsonData = json.decode(response.body);
      setState(() {
        pokemon = jsonData['pokemon'];
      });
    } else {
      print("error");
    }
}
```

将其转换为列表展示，下面是列表项的初始化：

```dart
List<Widget> _initView(){
    List<Widget> list = [];
    for (var poke in pokemon) {
      list.add(Text("pokemon: ${poke['name']}"));
    }
    return list;
}
```


### 一键切换主题

[Flutter 主题切换——让你的 APP 也能一键换肤 - 掘金 (juejin.cn)](https://juejin.cn/post/6844904137021194253)

使用 provider 和 flustars_flutter3 两个库。

首先确定想要切换的主题

```dart
Map<String, Color> themeColorMap = {
  'gray': Colors.grey,
  'blue': Colors.blue,
  'blueAccent': Colors.blueAccent,
  'cyan': Colors.cyan,
  'deepPurple': Colors.purple,
  'deepPurpleAccent': Colors.deepPurpleAccent,
  'deepOrange': Colors.orange,
  'green': Colors.green,
  'indigo': Colors.indigo,
  'indigoAccent': Colors.indigoAccent,
  'orange': Colors.orange,
  'purple': Colors.purple,
  'pink': Colors.pink,
  'red': Colors.red,
  'teal': Colors.teal,
  'black': Colors.black,
};
```

使用 Provider 进行全局状态管理

```dart
class AppInfoProvider with ChangeNotifier {
  String _themeColor = "";
  String get themeColor => _themeColor;

  setTheme(String themeColor){
    _themeColor = themeColor;
    notifyListeners();
  }
}
```

在 main.dart 配置创建的 provider，有多个状态管理就使用 MultiProvider，单个的使用 Provider.value：

```dart
class MyApp extends StatelessWidget {
  Color _themeColor = Colors.grey;
  MyApp({super.key});
  
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [ChangeNotifierProvider.value(value: AppInfoProvider())],
      child: Consumer<AppInfoProvider>(
        builder: (context, appInfo, child) {
          String colorKey = appInfo.themeColor;

          if (themeColorMap[colorKey] != null) {
            _themeColor = themeColorMap[colorKey]!;
          }
          return MaterialApp(
            title: 'Flutter Demo',
            // 重要的是对 ThemeData 的设置
            theme: ThemeData(
              primaryColor: _themeColor,
              floatingActionButtonTheme:
                  FloatingActionButtonThemeData(backgroundColor: _themeColor),
            ),
            home: const MyHomePage(title: 'Flutter Demo Home Page'),
          );
        },
      ),
    );
  }
}
```

如果需要改变主题，只需执行下面这行代码：

```dart
Provider.of<AppInfoProvider>(context, listen: false).setTheme(colorey);
```

关于 ThemeData 的设置：[ThemeData class - material library - Dart API (flutter.dev)](https://api.flutter.dev/flutter/material/ThemeData-class.html)

如果需要持久化选择的主题，需要使用 flustars_flutter3 中的 SpUtil，一般会在页面初始化加载的时候读取保存的颜色信息，所以我们需要在初始化页面配置如下代码：

```dart
String _colorKey;

@override
void initState() {
  super.initState();
  _initAsync();
}

Future<void> _initAsync() async {
  await SpUtil.getInstance();
  _colorKey = SpUtil.getString('key_theme_color', defValue: 'blue');
  // 设置初始化主题颜色
  Provider.of<AppInfoProvider>(context, listen: false).setTheme(_colorKey);
}
```

选择的代码为

```dart
setState(() {
  _colorKey = key;
});
SpHelper.putString('key_theme_color', key);
Provider.of<AppInfoProvider>(context).setTheme(key);
```

### 明暗切换

使用 adaptive_theme 库

使用 AdaptiveTheme 修饰 MaterialApp

```dart
import 'package:adaptive_theme/adaptive_theme.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return AdaptiveTheme(
      light: ThemeData.light(useMaterial3: true),
      dark: ThemeData.dark(useMaterial3: true),
      initial: AdaptiveThemeMode.light,
      builder: (theme, darkTheme) => MaterialApp(
        title: 'Adaptive Theme Demo',
        theme: theme,
        darkTheme: darkTheme,
        home: MyHomePage(),
      ),
    );
  }
}
```

切换主题的方法

```dart
// sets theme mode to dark
AdaptiveTheme.of(context).setDark();

// sets theme mode to light
AdaptiveTheme.of(context).setLight();

// sets theme mode to system default
AdaptiveTheme.of(context).setSystem();
```


设置主题

```dart
AdaptiveTheme.of(context).setTheme(
  light: ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    colorSchemeSeed: Colors.purple,
  ),
  dark: ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    colorSchemeSeed: Colors.purple,
  ),
);
```

### 为某个组件添加交互事件

某些组件本身并没有交互事件，如 Text 本身并没有点击事件，可以使用 GestureDetector 进行添加：

```dart
GestureDetector(
  onTap: () => Navigator.pushNamed(context, SignUpScreen.routeName),
  child: Text(
    "注册",
    style: TextStyle(
        fontSize: getProportionateScreenWidth(16),
        color: kPrimaryColor),
  ),
),
```

### 日志操作

使用 logger 和 path_provider（提供日志文件保存的路径）

创建一个方法获取 logger

```dart
import 'package:logger/logger.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';

Future<Logger> getLogger() async {
  final Directory appDocDir = await getApplicationDocumentsDirectory();
  String appDocPath = appDocDir.path;
  String logPath = "$appDocPath/app.log";
  Logger logger = Logger(
    output: MultiOutput(
      [ConsoleOutput(), FileOutput(file: File(logPath))]
    )
  );
  return logger;
}
```

在调用 logger 的时候需要初始化：

```dart
Logger logger = Logger();

// 注意 initState 不能带 async
@override
void initState() {
    super.initState();
    initLogger();
}
void initLogger() async{
	logger = await getLogger();
}

logger.t("Trace");
logger.d("Debug");
logger.i("Info");
logger.w("Warning");
logger.e("Error", error: 'Test Error');
logger.f("fatal", error: error, stackTrace: stackTrace);
```

读取日志文件：

```dart
final Directory appDocDir = await getApplicationDocumentsDirectory();
String appDocPath = appDocDir.path;
String logPath = "$appDocPath/app.log";
File file = File(logPath);
final contents = await file.readAsString();
print(contents);
```

## Getx 框架


Getx 框架集成了开发中许多重要内容（状态管理，依赖，路径等），这样方便开发。同时 Getx 简化了 flutter 中的许多设计，并且可以实现解耦视图和业务逻辑。

### 一个例子：实现点击计数

Getx 中使用 GetMaterialApp 替代 MaterialApp，跳转则使用 `Get.to()` 或者 `Get.back()` ，如 `Get.to(Other())` 表示跳转到 Other 界面。

Getx 通过设置一个控制器来管理变量和方法等，如果需要变量可见，则后标 `.obs`。这样的好处在变量改变时更新组件，不再需要 setState({})，而是直接用 `Obx` 修饰一个组件

```dart
class Controller extends GetxController{
  var count = 0.obs;
  increment() => count++;
}

class Home extends StatelessWidget {

  @override
  Widget build(context) {

    final Controller c = Get.put(Controller());

    return Scaffold(
      // Use Obx(()=> to update Text() whenever count is changed.
      appBar: AppBar(title: Obx(() => Text("Clicks: ${c.count}"))),
```

完整的示例如下

```dart
import 'package:flutter/material.dart';
import "package:get/get.dart";

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: Home()
    );
  }
}

class Controller extends GetxController {
  var count = 0.obs;
  increment() => count++;
}

class Home extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final Controller c = Get.put(Controller());
    return Scaffold(
      appBar: AppBar(
        title: Obx(() => Text("Clicks: ${c.count}")),
      ),
      body: Center(
        child: ElevatedButton(
            child: const Text("Go to Other"),
            onPressed: () {
              Get.to(Other());
            }),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: c.increment,
        child: const Icon(Icons.add),
      ),
    );
  }
}

class Other extends StatelessWidget {
  final Controller c = Get.find();

  @override
  Widget build(context) {
    return Scaffold(body: Center(child: Text("${c.count}")));
  }
}
```


### 状态管理

GetX 不像其他状态管理器那样使用 Streams 或 ChangeNotifier。为什么？除了为 android、 iOS、 web、 windows、 macos 和 linux 构建应用程序外，使用 GetX 还可以构建与 Flutter/GetX 语法相同的服务器应用程序。为了提高响应时间和降低内存消耗，Getx 创建了 GetValue 和 GetStream，这两个低延迟解决方案以较低的运营成本提供了大量的性能。我们使用这个基础来构建所有的资源，包括状态管理。

#### 反应式状态管理器

定义一个变量

```dart
var name = 'Jonatas Borges';
```

定义一个可观察的变量

```dart
var name = 'Jonatas Borges'.obs;
```

放在组件中

```dart
Obx (() => Text (controller.name));
```

该组件只会在 controller.name 变化时才变化。

除了将单个变量转为可观察变量，还可以将整个类转为可观察

```dart
class User {
  User({String name, int age});
  var name;
  var age;
}

// when instantianting:
final user = User(name: "Camila", age: 18).obs;
```

为变量设置监听器，最好在初始化函数 onInit 中使用

```dart
/// Called every time `count1` changes.
ever(count1, (_) => print("$_ has been changed"));

/// Called only first time the variable $_ is changed
once(count1, (_) => print("$_ was changed once"));

/// Anti DDos - Called every time the user stops typing for 1 second, for example.
debounce(count1, (_) => print("debouce$_"), time: Duration(seconds: 1));

/// Ignore all changes within 1 second.
interval(count1, (_) => print("interval $_"), time: Duration(seconds: 1));
```


#### 简单状态管理器

...

### 路由管理

导航至一个新的页面

```dart
Get.to(NextScreen());
```

导航至带名字的新页面

```dart
Get.toNamed('/details');
```


Navigator.pop(context)

```dart
Get.back();
```

转到下一个屏幕，不能选择回到上一个屏幕(用于 SplashScreens、登录屏幕等)

```dart
Get.off(NextScreen());
```

转到下一个屏幕并取消所有以前的路线(在购物车、轮询和测试中很有用)

```dart
Get.offAll(NextScreen());
```

## onnxruntime

[onnxruntime | Flutter package](https://pub.dev/packages/onnxruntime)

onnxruntime 用于在 flutter 中部署训练好的神经网络。

### 引用

将 onnx 后缀的模型放在 assets 文件夹中，并在 pubspec.yaml 中注明 assets 

```yaml
assets:  
  - assets/
```

如果在安卓中运行，那么大概率会遇到缺少 libonnxruntime.so 的错误，有两种解决方法：

1. 从 [Maven Repository: com.microsoft.onnxruntime » onnxruntime-android » 1.18.0 (mvnrepository.com)](https://mvnrepository.com/artifact/com.microsoft.onnxruntime/onnxruntime-android/latest) 下载对应的文件，下载文件的入口在表格的 Files 一栏中，下载 aar 文件，下载好后，将 aar 后缀改为 zip 后缀，解压后可以在 jni 文件夹找到 so 文件，将其复制到 build/app/intermediates/merged_native_libs 和 build/app/intermediates/stripped_native_libs 这两个文件夹。
2. 在 `android/app/build.gradle` 中添加 maven 依赖（和第一种解决方法中相同的地址），同时可能遇到 Execution failed for task ':app:mergeDebugNativeLibs' 错误，需要添加 packagingOptions
```json
android {  

    // 解决下面这个错误  
    // Execution failed for task ':app:mergeDebugNativeLibs'.  
    //> A failure occurred while executing com.android.build.gradle.internal.tasks.MergeNativeLibsTask$MergeNativeLibsTaskWorkAction    
    packagingOptions {  
        pickFirst 'lib/x86/libonnxruntime.so'  
        pickFirst 'lib/x86_64/libonnxruntime.so'  
        pickFirst 'lib/armeabi-v7a/libonnxruntime.so'  
        pickFirst 'lib/arm64-v8a/libonnxruntime.so'  
    }  
	//...
}  
dependencies {  
    implementation 'com.microsoft.onnxruntime:onnxruntime-android:1.20.0'  
}
```

注意第二种方法可能遇到 build\app\intermediates\flutter\debug\flutter_assets\assets 文件夹 model.onnx 无法自动删除导致错误，可以手动删除。或者在 `android/app/build.gradle` 添加删除任务

```json
android{
//...
}
task cleanTempFiles(type: Delete) {  
    delete fileTree(dir: '../../build/app/intermediates/flutter/debug/flutter_assets/assets', include: '*.onnx')
}  

preBuild.dependsOn cleanTempFiles
```

### 基本使用

在 `main.dart` 的 `initState` 初始化环境，在 `dispose` 时释放环境

```dart
// 需要在初始化模型之前初始化环境
void initOrtEnv(){  
  OrtEnv.instance.init();  
  OrtEnv.instance.availableProviders().forEach((element) {  
    print('onnx provider=$element');  
  });  
}

void releaseOrtEnv(){  
  OrtEnv.instance.release();  
}
```

可以将一个模型的推理过程放在一个类中，在这个类初始化模型，释放模型，完成推理

```dart
class Model{  
  OrtSessionOptions? _sessionOptions;  
  OrtSession? _session;  
  bool isInitialed = false;  
  
  var input2 = OrtValueTensor.createTensorWithDataList(Float32List.fromList(List.filled(64, 0.0)));  
  
  Model();  
    
  // 在 dispose() 时调用  
  release() {  
    _sessionOptions?.release();  
    _sessionOptions = null;  
    _session?.release();  
    _session = null;  
  }  
    
  // 在 initState() 时调用  
  Future<bool> initModel() async {  
    _sessionOptions = OrtSessionOptions()  
      ..setInterOpNumThreads(1)  
      ..setIntraOpNumThreads(1)  
      ..setSessionGraphOptimizationLevel(GraphOptimizationLevel.ortEnableAll);  
    final rawAssetFile = await rootBundle.load("assets/model.onnx");  
    final bytes = rawAssetFile.buffer.asUint8List();  
    _session = OrtSession.fromBuffer(bytes, _sessionOptions!);  
    return true;  
  }  
    
  // 重置状态  
  void reset(){  
    input2 = OrtValueTensor.createTensorWithDataList(Float32List.fromList(List.filled(64, 0.0)));  
  }  
    
  // 异步预测  
  Future<List<double>?> predictASync(List<List<int>> frames) {  
    return compute(predict, frames);  
  }  
    
  List<double>? predict(List<List<int>> frames) {  
      
    final input1 = OrtValueTensor.createTensorWithDataList(  
   Float32List.fromList(List.filled(64, 0.0)) , [1, 64]);
  
    final runOptions = OrtRunOptions();  
    final inputs = {"input1": input1, "input2": input2};  
    final List<OrtValue?>? outputs;  
  
    outputs = _session?.run(runOptions, inputs);  
    input1.release();  
    runOptions.release();  
  
    List<double> output1 = (outputs?[0]?.value as List<List<double>>)[0];
    input2 = OrtValueTensor.createTensorWithDataList(outputs?[1]?.value as List<double>);  
  
    outputs?.forEach((element) {  
      element?.release();  
    });  
  
    return output1;  
  }  
}
```



> [!NOTE] 
> 一般来说模型的输入需要是 Float32List，输出需要被转为类似 `List<double>` 类型



> [!NOTE] 
> 如果只需要语音识别、语音合成、说话人识别等语音相关功能，可以考虑使用 sherpa_onnx 库


### 在 Isolate 中推理

虽然大部分情况下使用 compute 就可以满足需要，但是部分场景（如每隔 10ms 调用一次模型）下可能会造成一些问题，可以将模型的推理放在 isolate 中。

首先定义 ReceivePort 和 SendPort

```dart
ReceivePort? receivePort;  
SendPort? sendPort;
```

在 initState 中初始化端口

```dart
receivePort = ReceivePort();  
receivePort?.listen((msg) {  
  if (msg is SendPort){  
    sendPort = msg;  
  }else if (msg is List<double>){  
    processCache = msg;  
  
    processStream.update(processCache);  
    setState(() {  
  
    });  
    Uint8List u8Data = doubleList2Uint8List(msg);  
    processFileStream?.update(u8Data);  
  }else if (msg == null){  
    print("result is null");  
  }  
});  
await Isolate.spawn(isolateTask, receivePort!.sendPort);  
  
final rawAssetFile = await rootBundle.load("assets/msa_dpcrn.onnx");  
final bytes = rawAssetFile.buffer.asUint8List();  
  
sendPort?.send(bytes);
```

需要注意的是模型只能在新开辟的 isolate 中初始化，并且由于在加载模型时需要使用 rootBundle，但是 rootBundle 只能在主 isolate 中使用，只能先加载好模型参数，将模型参数传入新的 isolate 中。

isolateTask 是静态函数，不能是类函数

```dart
void isolateTask(SendPort port) async {  
  // initOrtEnv();    // 不能放在这里，虽然不会报错，但是模型输出结果为null
  MsaDpcrn msaAce = MsaDpcrn();  
  
  final receivePort = ReceivePort();  
  port.send(receivePort.sendPort);  
  
  await for (var msg in receivePort) {  
    if (msg is String) {  
      if (msg == "exit") {  
        msaAce.release();  
        // port.send("will release");  
        // releaseOrtEnv(); 
        Isolate.exit(receivePort.sendPort);  
      } else if (msg == "reset") {  
        msaAce.reset();  
        // port.send("has reset");  
      }  
    } else if (msg is Uint8List) {  
      await msaAce.initModelByBuffer(msg);  
    } else if (msg is List<List<int>>) {  
      List<double>? result = msaAce.predictMultiFrames(msg);  
      port.send(result);  
    } else {  
      print("unknown msg type");  
    }  
  }  
}
```

>注意初始化 Onnx 环境和释放 Onnx 环境都需要在主 isolate 中实现，而不能在新开辟的 isolate 中实现

如果需要进行推理，通过 sendPort 传入数据

```dart
sendPort?.send([micFrame, refFrame]);
```


## 报错

> Invalid constant value.dart(invalid_constant)

可能是组件前面加上了 const 前缀


> No Material widget found. ListTile widgets require a Material widqet ancestor wtthin the closest LookupBoundary. In Material Design, most wdgets are conceptualy "printed" on a sheet of material. In Flutters material library, that material is represe nted by the Material widget it is the Materal widget that renders ink splashes, forinstance.Because of this, many material lbrary wldgets requt e that there be a Material widget in the tree above them.

使用的组件没有被 Material 组件（Material、Scaffold 等）包裹。


> RenderFlex children have non-zero flex but incoming height constraints are unbounded.

给 Flex 组件外侧套一层 Container 并设定高度


> Vertical viewport was given unbounded height.

可能是因为使用 ListView 出现的问题，需要在 ListView 中加入 shrinkWrap: true

```dart
ListView(
    shrinkWrap: true,
    children: _initView(),
)
```




