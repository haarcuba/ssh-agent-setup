require 'yaml'
require 'logger'

$log = Logger.new STDERR



task :units do
    sh "python -m pytest -sv tests/"
end

desc "make sure we did not forget to include any tests"
task :all_tests_included do
  $log.info "Verifying that we did not forget any dependencies for the All-OK job"
  tests = YAML.load_file '.github/workflows/tests.yaml'
  check_names = tests["jobs"].keys.filter {|job| job != 'All-OK'}
  all_ok = tests['jobs']['All-OK']
  dependencies = all_ok['needs'].to_set
  missing_jobs = check_names.to_set - dependencies
  fail("FAILURE: All-OK missing some tests: #{missing_jobs.to_a}") if missing_jobs.size > 0
  $log.info "no forgotten dependencies, all jobs are included"

  step_names = all_ok['steps'].map {|step| step["name"]}
  missing_jobs = dependencies - step_names.to_set
  fail("FAILURE: All-OK step-by-step verification missing some tests: #{missing_jobs.to_a}") if missing_jobs.size > 0
  $log.info "verified: a step exists for each of the dependencies"

  all_ok['steps'].each do |step|
    name = step['name']
    next if ! dependencies.include?(name)
    command = step['run']
    referenced = command.include?(name)
    fail("FAILURE: step command for #{name} does not reference '#{name}'") if !referenced
  end
  $log.info "verified: each step references its own dependency"
end

task :enforce_success, [:status] do |t, args|
  status = args[:status]
  fail("FAILURE: received '#{status}' only 'success' is acceptable!") if status != 'success'
end
