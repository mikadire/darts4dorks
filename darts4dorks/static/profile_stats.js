document.addEventListener("DOMContentLoaded", () => {
  const errorMessage = document.getElementById("error-message");

  createChart(data);

  function cumulativeAverage(data) {
    const result = [];
    let runningSum = 0;

    for (let i = 0; i < data.length; i++) {
      runningSum += data[i];
      const avg = runningSum / (i + 1);
      result.push(avg);
    }

    return result;
  }

  function createChart(data) {
    const sessionDate = data.temporal_session_stats.map((point) => {
      const date = new Date(point.date);
      return date.toLocaleString();
    });

    const sessionAvg = data.temporal_session_stats.map(
      (point) => point.avg_darts_thrown
    );
    const rollingSessionAvg = cumulativeAverage(sessionAvg);

    const targetsDict = data.temporal_target_stats.reduce((acc, row) => {
      if (!acc[row.target]) {
        acc[row.target] = { date: [], darts_thrown: [] };
      }
      acc[row.target].date.push(row.date);
      acc[row.target].darts_thrown.push(row.darts_thrown);
      return acc;
    }, {});

    const sessionTrace = {
      x: sessionDate,
      y: rollingSessionAvg,
      name: "Running average",
      type: "lines",
      color: "black",
      line: {
        color: "black",
        width: 7,
      },
    };

    const targetTraces = Object.entries(targetsDict).map(
      ([target, values]) => ({
        x: values.date.map((point) => new Date(point).toLocaleString()),
        y: values.darts_thrown,
        name: target === "21" ? "Bull" : `Target: ${target}`,
        type: "scatter",
      })
    );

    const traces = targetTraces.concat(sessionTrace);

    const config = { responsive: true };

    const layout = {
      xaxis: { title: { text: "Session" } },
      yaxis: { title: { text: "Darts Thrown" }, zeroline: true },
      showlegend: true,
    };

    Plotly.newPlot("chart", traces, layout, config);
  }
});
