from flask import Flask, render_template,request
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# Load the cleaned dataset
df = pd.read_csv("data/cleaned_data.csv")
df['Date'] = pd.to_datetime(df['Date'])

# State columns
state_columns = [col for col in df.columns if col not in ['Date', 'Total', 'Year', 'Month']]
def create_top10_chart(data, selected_state="all"):

    if selected_state != "all" and selected_state in state_columns:

        state_average = data[selected_state].mean()

        chart_data = pd.Series(
            {selected_state: state_average}
        )

        title = f"{selected_state} - Average Value"

    else:

        state_averages = data[state_columns].mean()

        chart_data = (
            state_averages
            .sort_values(ascending=False)
            .head(10)
        )

        title = "Top 10 States by Average Value"

    plt.figure(figsize=(8, 3))

    chart_data.sort_values().plot(
        kind="barh",
        color="#14B8A6"
    )

    plt.title(title)
    plt.xlabel("Average Value")
    plt.ylabel("State")

    plt.tight_layout()

    plt.savefig("static/charts/top10_states.png")
    plt.close()
def create_daily_trend_chart(data, selected_state="all"):

    plt.figure(figsize=(8, 3.5))

    if selected_state != "all" and selected_state in state_columns:

        plt.plot(
            data['Date'],
            data[selected_state],
            color='#14B8A6',
            linewidth=2
        )

        title = f"{selected_state} Daily Trend"
        ylabel = "Average Value"

    else:

        plt.plot(
            data['Date'],
            data['Total'],
            color='#14B8A6',
            linewidth=2
        )

        title = "Overall daily Trend"
        ylabel = "Total Value"

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(ylabel)

    plt.xticks(rotation=45)

    plt.gca().xaxis.set_major_locator(
        plt.matplotlib.dates.MonthLocator()
    )

    plt.gca().xaxis.set_major_formatter(
        plt.matplotlib.dates.DateFormatter('%b %Y')
    )

    plt.tight_layout()

    plt.savefig("static/charts/daily_trend.png")
 
def create_year_comparison_chart(data, selected_state="all"):

    if selected_state != "all" and selected_state in state_columns:

        yearly_average = data.groupby('Year')[selected_state].mean()

        title = f"{selected_state} - Year-wise Average Value"

    else:

        yearly_average = data.groupby('Year')['Total'].mean()

        title = "Year-wise Average Value"

    plt.figure(figsize=(10, 8))

    yearly_average.plot(
        kind='bar',
        color='#14B8A6'
    )

    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Average Value")

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig("static/charts/year_comparison.png")
    plt.close()
def create_distribution_chart(data, selected_state="all"):

    plt.figure(figsize=(12, 9))

    if selected_state != "all" and selected_state in state_columns:

        plt.hist(
            data[selected_state],
            bins=20,
            color='#14B8A6',
            edgecolor='white'
        )

        title = f"{selected_state} - Value Distribution"

    else:

        plt.hist(
            data['Total'],
            bins=20,
            color='#14B8A6',
            edgecolor='white'
        )

        title = "Overall Value Distribution"

    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig("static/charts/distribution.png")
    plt.close()
def create_correlation_chart(data):

    correlation = data[state_columns].corr()

    plt.figure(figsize=(12, 9))

    sns.heatmap(
    correlation,
    cmap="coolwarm",
    center=0,
    annot=False,
    linewidths=0.2
)

    plt.title("State-wise Correlation Heatmap")

    plt.tight_layout()

    plt.savefig("static/charts/correlation.png")
    plt.close()
def create_state_comparison_chart(data):

    state_averages = data[state_columns].mean().sort_values()

    plt.figure(figsize=(10, 8))

    state_averages.plot(
        kind="barh",
        color="#14B8A6"
    )

    plt.title("State-wise Energy Comparison")
    plt.xlabel("Average Energy Value")
    plt.ylabel("State / UT")

    plt.tight_layout()

    plt.savefig("static/charts/state_comparison.png")
    plt.close()

    print("State-wise comparison chart created")
def create_peak_anomaly_chart(data):

    mean_value = data['Total'].mean()
    std_value = data['Total'].std()

    upper_limit = mean_value + 2 * std_value
    lower_limit = mean_value - 2 * std_value

    anomalies = data[
        (data['Total'] > upper_limit) |
        (data['Total'] < lower_limit)
    ]

    plt.figure(figsize=(8, 2.5))

    plt.plot(
        data['Date'],
        data['Total'],
        color='#14B8A6',
        linewidth=1.5
    )

    plt.scatter(
        anomalies['Date'],
        anomalies['Total'],
        color='red',
        label='Potential Anomaly'
    )

    plt.axhline(
        upper_limit,
        linestyle='--',
        label='Upper Limit'
    )

    plt.axhline(
        lower_limit,
        linestyle='--',
        label='Lower Limit'
    )

    plt.title("Peak & Anomaly Analysis",fontsize=7)
    plt.xlabel("Date",fontsize=7)
    plt.ylabel("Total Value",fontsize=7)
    plt.legend(fontsize=7)

    plt.xticks(rotation=45,fontsize=7)
    plt.yticks(fontsize=7)

    plt.tight_layout()

    plt.savefig("static/charts/peak_anomaly.png")
    plt.close()
    print("Peak anomaly chart created")
@app.route("/")
def dashboard():
    create_top10_chart(df)
    create_daily_trend_chart(df)
    create_year_comparison_chart(df)
    create_distribution_chart(df)
    create_correlation_chart(df)
    create_state_comparison_chart(df)
    create_peak_anomaly_chart(df)
    # Calculate dashboard values
    total_states = len(state_columns)
    avg_total = round(df['Total'].mean(), 2)
    peak_total = round(df['Total'].max(), 2)

    # Find state with highest average value
    state_averages = df[state_columns].mean()
    top_state = state_averages.idxmax()
    top_state_avg = round(state_averages.max(), 2)

    # Send data to HTML
    return render_template(
        "index.html",
        total_states=total_states,
        avg_total=avg_total,
        peak_total=peak_total,
        top_state=top_state,
        top_state_avg=top_state_avg,
        states=sorted(state_columns),
        years=sorted(df['Year'].unique())
    )
@app.route("/analysis")
def analysis():

    selected_state = request.args.get("state", "all")
    selected_year = request.args.get("year", "all")
    selected_analysis = request.args.get("analysis_type", "average")

    filtered_df = df.copy()

    # Apply year filter only if a specific year is selected
    if selected_year != "all":
        filtered_df = filtered_df[
            filtered_df["Year"].astype(str) == selected_year
        ]

    # Apply state filter only if a specific state is selected
    if selected_state != "all" and selected_state in state_columns:
        state_average = round(filtered_df[selected_state].mean(), 2)
        top_state = selected_state
        top_state_avg = state_average
    else:
        state_averages = filtered_df[state_columns].mean()
        top_state = state_averages.idxmax()
        top_state_avg = round(state_averages.max(), 2)
            # Calculate selected analysis value
    if selected_analysis == "maximum":
        analysis_value = round(filtered_df["Total"].max(), 2)

    elif selected_analysis == "trend":
        analysis_value = round(filtered_df["Total"].iloc[-1], 2)

    elif selected_analysis == "distribution":
        analysis_value = round(filtered_df["Total"].median(), 2)

    else:
        analysis_value = round(filtered_df["Total"].mean(), 2)

    create_top10_chart(filtered_df, selected_state)
    create_daily_trend_chart(filtered_df, selected_state)
    create_year_comparison_chart(filtered_df, selected_state)
    create_distribution_chart(filtered_df, selected_state)
    

    return render_template(
    "index.html",
    total_states=len(state_columns),
    avg_total=round(filtered_df["Total"].mean(), 2),
    peak_total=round(filtered_df["Total"].max(), 2),
    top_state=top_state,
    top_state_avg=top_state_avg,
    states=sorted(state_columns),
    years=sorted(df["Year"].unique()),
    selected_state=selected_state,
    selected_year=selected_year,
    selected_analysis=selected_analysis,
    analysis_value=analysis_value
)

    

if __name__ == "__main__":
    import os
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )