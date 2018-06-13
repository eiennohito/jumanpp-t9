//
// Created by Arseny Tolmachev on 2018/06/11.
//

#include "core/env.h"
#include "core/analysis/analysis_result.h"
#include "jumanpp_t9.spec.h"

#include <iostream>
#include <string>

using namespace jumanpp;


struct ResultOutputter {
  core::analysis::StringField surface;
  core::analysis::StringField english;

  core::analysis::AnalysisResult resultFiller;
  core::analysis::AnalysisPath top1;

  Status initialize(const core::analysis::Analyzer& ana) {
    auto& output = ana.output();
    JPP_RETURN_IF_ERROR(output.stringField("surface", &surface));
    JPP_RETURN_IF_ERROR(output.stringField("english", &english));
    return Status::Ok();
  }

  bool outputResult(const core::analysis::Analyzer& ana, std::ostream& os) {
    if (!resultFiller.reset(ana)) return false;
    if (!resultFiller.fillTop1(&top1)) return false;

    auto& output = ana.output();
    core::analysis::NodeWalker walker;

    core::analysis::ConnectionPtr cptr{};
    while (top1.nextBoundary()) {
      if (!top1.nextNode(&cptr) || !output.locate(cptr.latticeNodePtr(), &walker) || !walker.next()) {
        return false;
      }

      os << surface[walker] << "\t" << english[walker] << "\n";
    }
    os << std::endl;
    return true;
  }
};

void dieOnError(Status s) {
  if (!s) {
    std::cerr << s;
    exit(1);
  }
}

int main(int argc, const char* argv[]) {
  core::JumanppEnv env;
  dieOnError(env.loadModel(StringPiece::fromCString(argv[1])));

  env.setBeamSize(5);
  env.setGlobalBeam(6, 1, 5);

  jumanpp_generated::JppT9Static cg;
  dieOnError(env.initFeatures(&cg));

  core::analysis::Analyzer analyzer;

  dieOnError(env.makeAnalyzer(&analyzer));

  ResultOutputter out;
  dieOnError(out.initialize(analyzer));

  std::string input;
  while (std::getline(std::cin, input)) {
    Status s = analyzer.analyze(input);
    if (!s) {
      std::cerr << "Failed to analyze [" << input << "]: " << s;
      continue;
    }
    out.outputResult(analyzer, std::cout);
  }

  return 0;
}