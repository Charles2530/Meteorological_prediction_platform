export interface WeatherData {
  pid: number;
  city: string;
  temperature: number;
  humidity: number;
  windSpeed: number;
}

export interface NotificationData {
  id: number;
  img: string;
  title: string;
  date: string;
  city: string;
  level: number;
  content: string;
  instruction: string;
}

export interface NotificationNotice {
  id: number;
  img: string;
  title: string;
  date: string;
  city: string;
}

export interface GetSubscribeResponse {
  tableData: { city: string; status: string }[];
}

export interface AqiRankItem {
  city: string;
  category: string;
  aqi: number;
}

export interface CityWeatherData {
  time: string;
  city: string;
  temp: number;
  text: string;
  precip: number;
  wind360: number;
  windScale: number;
  windSpeed: number;
  humidity: number;
  pressure: number;
  aqi: number;
  category: string;
}

export interface ProInfo {
  weather: {
    icoid: string,
    time: string;
    tem: string;
    condition: string;
    infos: string;
    wind: string;
    windDir: string;
    hum: string;
    ray: string;
    air: string;
    airAQI: string;
    visibility: string;
    rainfall: string;
    pressure: string;
  },
  geography: string;
  hazardTable: Array<{
    place: string;
    level: string;
    type: string;
  }>;
}

export interface Hazard {
  place: string;
  longitude: number;
  latitude: number;
  type: string;
  time:string;
  level: string;
}
