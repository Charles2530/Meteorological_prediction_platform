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
}
