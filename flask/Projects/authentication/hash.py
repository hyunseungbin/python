import hashlib
import bcrypt

m = hashlib.sha256()

## b는 바이트 형태로 전환
## 해쉬를 사용하기 위해서는 바이트형태여야 한다.
m.update(b"test password")
m.hexdigest

## bcrypt 는 해쉬 형태에서 salting과 키 스트레칭을 통해 복호화가 어렵고 불가능에 가깝게 만들수 있다.
## gensalt 를 통해 salting 을 실행 하여 개발자 조차 해당 값을 알 수 없게 한다.
## b'$2b$12$E5TSTU1kP0moCZAs8ZVRzOOwPAY4ttFNqWC0VkJH5jbpue7muXeN.'
bcrypt.hashpw(b"secret password", bcrypt.gensalt())

## salting 한 값에 16진수로 변환하여 더욱 복잡하게 만들수 있다.
bcrypt.hashpw(b"secret password", bcrypt.gensalt()).hex()
