document.addEventListener("DOMContentLoaded", () => {
  const errorMessage = document.getElementById("error-message");

  //   fetchStats(userId);

  async function fetchStats(userId) {
    try {
      const response = await fetch(`/rtc_stats/${userId}`);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          `Response status: ${response.status}, Error: ${errorData.message}`
        );
      }

      const data = await response.json();
      createChart(data);
    } catch (error) {
      console.error(error.message);
      errorMessage.textContent = `Failed to load statistics. Please try again.`;
    }
  }

  //   function createPlotlyChart(data) {
  //     const date = data.temporal_session_stats.map((point) => point.date);
  //     const sessionAvg = data.temporal_session_stats.map(
  //       (point) => point.avg_darts_thrown
  //     );

  //     const sessionTrace = {
  //       x: date,
  //       y: sessionAvg,
  //       type: "line",
  //       marker: { color: "rgba(0, 0, 255, 0.6)" },
  //     };

  //     const layout = {
  //         xaxis: { title: "Date" },
  //         yaxis: { title: "Darts Thrown", zeroline: true },
  //         barmode: "group",
  //         bargap: 0.2,
  //       };

  //     const config = { responsive: true };

  //     const dataPlotly = [sessionTrace];

  //     Plotly.newPlot("darts-chart", dataPlotly, layout, config);
  //   }
  // Function to generate the fake data
  // Function to generate the fake data
  function generateFakeData() {
    const x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    const y1 = x.map((x) => Math.sin(x) * 10); // Dataset 1: Sin wave
    const y2 = x.map((x) => Math.cos(x) * 10); // Dataset 2: Cos wave
    const y3 = x.map((x) => (x - 5) * 3); // Dataset 3: Linear relationship

    return { x, y1, y2, y3 };
  }

  // Function to create a trace for each dataset
  function makeTrace(i) {
    const data = generateFakeData();
    const yData = data[`y${i + 1}`]; // y1, y2, or y3 based on index
    return {
      x: data.x,
      y: yData,
      mode: "lines",
      name: `Data set ${i + 1}`,
      line: {
        shape: "spline",
        color: i === 0 ? "blue" : i === 1 ? "green" : "red",
      },
      visible: i === 0, // Only the first dataset is visible initially
    };
  }

  // Create the chart with the traces and updatemenus for interactivity
  function createChart() {
    const traces = [0, 1, 2].map(makeTrace);

    const layout = {
      title: "Dynamic Line Chart with Datasets",
      xaxis: { title: "X Axis" },
      yaxis: { title: "Y Axis" },
      updatemenus: [
        {
          y: 0.8,
          yanchor: "top",
          buttons: [
            {
              method: "restyle",
              args: ["line.color", "red"],
              label: "Red",
            },
            {
              method: "restyle",
              args: ["line.color", "blue"],
              label: "Blue",
            },
            {
              method: "restyle",
              args: ["line.color", "green"],
              label: "Green",
            },
          ],
        },
        {
          y: 1,
          yanchor: "top",
          buttons: [
            {
              method: "restyle",
              args: ["visible", [true, false, false]],
              label: "Data set 1",
            },
            {
              method: "restyle",
              args: ["visible", [false, true, false]],
              label: "Data set 2",
            },
            {
              method: "restyle",
              args: ["visible", [false, false, true]],
              label: "Data set 3",
            },
            {
              method: "restyle",
              args: ["visible", [true, true, true]],
              label: "Display All",
            }, // New option to show all datasets
          ],
        },
      ],
    };

    Plotly.newPlot("line-chart", traces, layout);
  }

  // Initialize the chart
  createChart();
});
