export const translateTime = (inputDate) => {
    if (!inputDate) { return }
    const date = new Date(inputDate);

    // 获取小时
    const hour = date.getHours();

    // 获取星期
    const daysOfWeek = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    const dayOfWeek = daysOfWeek[date.getUTCDay()];

    // 获取日期
    // const options = { year: 'numeric', month: 'long', day: 'numeric' };
    // const formattedDate = date.toLocaleDateString('zh-CN', options);
    // 获取月份和日期
    const month = (date.getMonth() + 1).toString(); // 月份从0开始，因此需要加1
    const day = date.getDate().toString();

    // 格式化为 "MM/DD" 格式
    const formattedDate = `${month.padStart(2, '0')}/${day.padStart(2, '0')}`

    // return `${dayOfWeek} ${formattedDate}`
    return {
        dayOfWeek,
        formattedDate,
        hour
    }
}

export const formatDate = (date) => {
    const queryDate = new Date(date)
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);

    if (queryDate.toDateString() === today.toDateString()) {
        return "今天";
    } else if (queryDate.toDateString() === yesterday.toDateString()) {
        return "昨天";
    } else if (queryDate.toDateString() === tomorrow.toDateString()) {
        return "明天";
    } else {
        const daysOfWeek = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
        return daysOfWeek[queryDate.getDay()];
    }
}

export const getPreFormattedDate = () => {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);

    const year = yesterday.getFullYear();
    const month = String(yesterday.getMonth() + 1).padStart(2, '0'); // 月份从0开始，需要加1，并确保是两位数
    const day = String(yesterday.getDate()).padStart(2, '0'); // 日期需要确保是两位数

    const formattedDate = `${year}${month}${day}`;
    return formattedDate;
}

export const findMostFrequentItem = (arr) => {
    if (arr.length === 0) {
        return null; // 空数组，没有出现次数最多的项
    }

    const itemFrequencyMap = new Map();

    // 遍历数组并统计每个项出现的次数
    for (const item of arr) {
        if (itemFrequencyMap.has(item)) {
            itemFrequencyMap.set(item, itemFrequencyMap.get(item) + 1);
        } else {
            itemFrequencyMap.set(item, 1);
        }
    }

    let mostFrequentItem = arr[0];
    let maxFrequency = itemFrequencyMap.get(arr[0]);

    // 遍历项和它们的出现次数，找到出现次数最多的项
    for (const [item, frequency] of itemFrequencyMap) {
        if (frequency > maxFrequency) {
            mostFrequentItem = item;
            maxFrequency = frequency;
        }
    }

    return mostFrequentItem
}

// export const getDateToday = () => {
//     // 获取当前时间
//     const currentDate = new Date();
//     // 将时间格式化为英文形式
//     const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
//     const formattedDate = currentDate.toLocaleDateString('en-US', options);
//     return formattedDate;
// }

export const getDateToday = () => {
    // 获取当前时间
    const currentDate = new Date();
    // 分别获取年、月、日
    const year = currentDate.getFullYear(); // 获取年份的后两位
    const month = (currentDate.getMonth() + 1).toString().padStart(2, '0'); // 月份从 0 开始，需要加 1
    const day = currentDate.getDate().toString().padStart(2, '0');
  
    // 拼接成 yy-mm-dd 格式
    return `${year}-${month}-${day}`;
  };