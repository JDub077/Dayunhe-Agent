import axios from 'axios'

const client = axios.create({
  baseURL: '/api/v1',
  timeout: 35000,
  headers: {
    'Content-Type': 'application/json',
  },
})

client.interceptors.response.use(
  (res) => res.data,
  (err) => {
    if (err.code === 'ECONNABORTED') {
      return Promise.resolve({
        code: -1,
        message: 'timeout',
        data: { content: '（角色望着河水，一时陷入沉思……）' },
      })
    }
    return Promise.reject(err)
  }
)

export default client
