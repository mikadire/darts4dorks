document.addEventListener("DOMContentLoaded", () => {
  const errorMessage = document.getElementById("error-message");
  const lifetimeStatsDiv = document.getElementById("lifetime-stats");
  const sessionStatsDiv = document.getElementById("session-stats");

  displayStats(data);
  createChart(data);

  function displayStats(data) {
    const lifetimeHtml = `
      <p><strong>Lifetime Average per Target:</strong> ${data.lifetime_stats.avg_darts_thrown.toFixed(
        2
      )}</p>
      <p><strong>Lifetime Standard Deviation:</strong> ${data.lifetime_stats.stddev_darts_thrown.toFixed(
        2
      )}</p>
    `;
    lifetimeStatsDiv.innerHTML = lifetimeHtml;

    const sessionHtml = `
      <p><strong>Average Darts Thrown per Target:</strong> ${data.temporal_session_stats
        .find((stat) => stat.session_id === sessionId)
        .avg_darts_thrown.toFixed(2)}</p>
      <p><strong>Standard Deviation:</strong> ${data.temporal_session_stats
        .find((stat) => stat.session_id === sessionId)
        .stddev_darts_thrown.toFixed(2)}</p>
    `;
    sessionStatsDiv.innerHTML = sessionHtml;
  }

  function createChart(data) {
    const targets = data.lifetime_target_stats.map((point) => point.target);
    const modifiedTargets = targets.map((target) =>
      target === 21 ? "Bull" : target
    );

    const sessionDarts = data.temporal_target_stats
      .filter((stat) => stat.session_id == sessionId)
      .map((stat) => stat.darts_thrown);
    const lifetimeAvgs = data.lifetime_target_stats.map(
      (stat) => stat.avg_darts_thrown
    );
    const lifetimeStdDevs = data.lifetime_target_stats.map((stat) =>
      stat.stddev_darts_thrown.toFixed(2)
    );

    const sessionTrace = {
      x: modifiedTargets,
      y: sessionDarts,
      name: "This Game",
      type: "bar",
      marker: { color: "rgb(13, 110, 253)" },
    };

    const lifetimeTrace = {
      x: modifiedTargets,
      y: lifetimeAvgs,
      name: "Lifetime Avg",
      type: "bar",
      marker: { color: "rgb(204,0,204)" },
      error_y: {
        type: "data",
        name: "Standard deviation",
        symmetric: false,
        array: lifetimeStdDevs,
        arrayminus: lifetimeAvgs.map((avg, index) =>
          Math.min(avg, lifetimeStdDevs[index])
        ),
        color: "black",
        thickness: 2,
        width: 8,
      },
    };

    const traces = [sessionTrace, lifetimeTrace];

    const layout = {
      xaxis: {
        title: { text: "Targets" },
        tickvals: modifiedTargets,
        type: "category",
      },
      yaxis: { title: { text: "Darts Thrown" }, zeroline: true },
      barmode: "group",
      bargap: 0.2,
    };

    const config = { responsive: true };

    Plotly.newPlot("chart", traces, layout, config);
  }
});
