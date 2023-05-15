import { RNCamera } from 'react-native-camera';
import axios from 'axios';

// ...

// 영상을 촬영하고 Django 서버로 전송하는 함수
const captureAndSendVideo = async () => {
  if (this.camera) {
    const options = { quality: 0.5, base64: true };
    const data = await this.camera.recordAsync(options);

    // Django 서버로 POST 요청을 보냄
    axios.post('http://your-django-server.com/process-video', {
      video: data.base64,
    })
      .then(response => {
        console.log('영상 전송 성공:', response.data);
      })
      .catch(error => {
        console.error('영상 전송 실패:', error);
      });
  }
};

// ...

// RNCamera 컴포넌트를 사용하여 영상 촬영 버튼과 이벤트 핸들러를 생성
<RNCamera
  ref={ref => {
    this.camera = ref;
  }}
  style={styles.preview}
>
  <View style={{ flex: 0, flexDirection: 'row', justifyContent: 'center' }}>
    <TouchableOpacity onPress={captureAndSendVideo}>
      <Text style={{ fontSize: 14 }}>영상 촬영</Text>
    </TouchableOpacity>
  </View>
</RNCamera>