import streamlit as st
import pandas as pd
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt

def run_bayesian_ab_test(control_data, treatment_data):
    with pm.Model() as model:
        # Priors
        p_control = pm.Beta('p_control', alpha=1, beta=1)
        p_treatment = pm.Beta('p_treatment', alpha=1, beta=1)

        # Likelihoods
        control_obs = pm.Bernoulli('control_obs', p=p_control, observed=control_data)
        treatment_obs = pm.Bernoulli('treatment_obs', p=p_treatment, observed=treatment_data)

     

        # In your model function
        trace = pm.sample(draws=100, tune=100, chains=1, cores=1, 
                  init="adapt_diag", target_accept=0.9, progressbar=False)
        ##trace = pm.sample(draws=300, tune=200,chains=1,cores=1, init="adapt_diag",   target_accept=0.9, progressbar=False)

    return trace

# Streamlit UI
st.title("Bayesian A/B Testing App")

uploaded_file = st.file_uploader("cookie_cats", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Optional: Subsample for faster execution
    df = df.sample(n=min(1000, len(df)), random_state=42)

    # Display raw data
    st.subheader("Raw Data")
    st.write(df.head())

    # Map version to 0 and 1 if necessary
    if 'version' in df.columns:
        df['version_code'] = df['version'].map({'gate_30': 0, 'gate_40': 1})
    elif 'version_code' not in df.columns:
        st.error("Expected 'version' or 'version_code' column in CSV.")
    else:
        pass  # version_code already exists

    if 'retention_1' not in df.columns:
        st.error("Expected 'retention_1' column in CSV.")
    else:
        # Split into groups
        control_data = df[df['version_code'] == 0]['retention_1'].values
        treatment_data = df[df['version_code'] == 1]['retention_1'].values

        if len(control_data) == 0 or len(treatment_data) == 0:
            st.error("One of the groups is empty.")
        else:
            st.success("Running Bayesian A/B Test...")

            trace = run_bayesian_ab_test(control_data, treatment_data)

            st.subheader("Posterior Distributions")
            fig, ax = plt.subplots()
            az.plot_posterior(trace, var_names=['p_control', 'p_treatment'], ax=ax)
            st.pyplot(fig)

            # Prob treatment better than control
            p_c = trace.posterior['p_control'].values.flatten()
            p_t = trace.posterior['p_treatment'].values.flatten()
            prob = (p_t > p_c).mean()

           
            st.metric(label="P(p_treatment > p_control)", value=f"{prob:.2%}")
